import Foundation
import Darwin

/// One newline-delimited JSON request/response per connection, accessible to this user only.
final class ControlServer {
    static let maximumRequestBytes = 256 * 1024
    private let path: String
    private let handler: ([String: Any]) -> [String: Any]
    private var listener: Int32 = -1

    init(path: String, handler: @escaping ([String: Any]) -> [String: Any]) {
        self.path = path
        self.handler = handler
    }

    func start() throws {
        let directory = URL(fileURLWithPath: path).deletingLastPathComponent().path
        try FileManager.default.createDirectory(atPath: directory, withIntermediateDirectories: true,
                                               attributes: [.posixPermissions: 0o700])
        var directoryInfo = stat()
        guard lstat(directory, &directoryInfo) == 0, directoryInfo.st_uid == getuid(),
              directoryInfo.st_mode & mode_t(S_IFMT) == mode_t(S_IFDIR), chmod(directory, 0o700) == 0 else {
            throw failure("Control directory must be a private directory owned by this user.")
        }
        var address = sockaddr_un()
        let bytes = Array(path.utf8) + [UInt8(0)]
        guard bytes.count <= MemoryLayout.size(ofValue: address.sun_path) else {
            throw failure("Control socket path is too long.")
        }
        address.sun_family = sa_family_t(AF_UNIX)
        address.sun_len = UInt8(MemoryLayout<sockaddr_un>.size)
        withUnsafeMutableBytes(of: &address.sun_path) { target in
            target.copyBytes(from: bytes)
        }

        var existing = stat()
        if lstat(path, &existing) == 0 {
            guard existing.st_mode & mode_t(S_IFMT) == mode_t(S_IFSOCK), existing.st_uid == getuid() else {
                throw failure("Refusing to replace an unexpected file at the control socket path.")
            }
            let probe = socket(AF_UNIX, SOCK_STREAM, 0)
            guard probe >= 0 else { throw failure("Cannot check the existing control socket.") }
            let connected = withUnsafePointer(to: &address) {
                $0.withMemoryRebound(to: sockaddr.self, capacity: 1) {
                    connect(probe, $0, socklen_t(MemoryLayout<sockaddr_un>.size)) == 0
                }
            }
            let connectError = errno
            Darwin.close(probe)
            guard !connected else { throw failure("Another Brain instance already owns the control socket.") }
            guard connectError == ECONNREFUSED || connectError == ENOENT else {
                throw failure("Cannot verify whether the existing control socket is active.")
            }
            guard unlink(path) == 0 || errno == ENOENT else { throw failure("Cannot remove stale control socket.") }
        }

        let fd = socket(AF_UNIX, SOCK_STREAM, 0)
        guard fd >= 0 else { throw failure("Cannot create control socket.") }
        _ = fcntl(fd, F_SETFD, FD_CLOEXEC)
        let bound = withUnsafePointer(to: &address) {
            $0.withMemoryRebound(to: sockaddr.self, capacity: 1) {
                bind(fd, $0, socklen_t(MemoryLayout<sockaddr_un>.size)) == 0
            }
        }
        guard bound else { Darwin.close(fd); throw failure("Cannot bind control socket.") }
        guard chmod(path, 0o600) == 0, listen(fd, 8) == 0 else {
            Darwin.close(fd); unlink(path); throw failure("Cannot start private control socket.")
        }
        listener = fd
        DispatchQueue(label: "brain.control.accept").async { [weak self] in
            while true {
                let client = accept(fd, nil, nil)
                if client < 0 {
                    if errno == EINTR { continue }
                    break
                }
                guard let self else { Darwin.close(client); break }
                _ = fcntl(client, F_SETFD, FD_CLOEXEC)
                self.serve(client)
                Darwin.close(client)
            }
        }
    }

    func stop() {
        guard listener >= 0 else { return }
        shutdown(listener, SHUT_RDWR)
        Darwin.close(listener)
        listener = -1
        unlink(path)
    }

    private func serve(_ client: Int32) {
        var peerUID: uid_t = 0, peerGID: gid_t = 0
        guard getpeereid(client, &peerUID, &peerGID) == 0, peerUID == getuid() else { return }
        var timeout = timeval(tv_sec: 3, tv_usec: 0)
        setsockopt(client, SOL_SOCKET, SO_RCVTIMEO, &timeout, socklen_t(MemoryLayout<timeval>.size))
        setsockopt(client, SOL_SOCKET, SO_SNDTIMEO, &timeout, socklen_t(MemoryLayout<timeval>.size))
        var data = Data()
        var buffer = [UInt8](repeating: 0, count: 4096)
        while data.count <= Self.maximumRequestBytes {
            let count = Darwin.read(client, &buffer, buffer.count)
            guard count > 0 else { return }
            data.append(contentsOf: buffer.prefix(count))
            if let newline = data.firstIndex(of: 10) {
                guard newline <= Self.maximumRequestBytes else { break }
                let response: [String: Any]
                if let request = try? JSONSerialization.jsonObject(with: data.prefix(upTo: newline)) as? [String: Any] {
                    response = DispatchQueue.main.sync { handler(request) }
                } else {
                    response = Self.error("invalid_request", "Expected one JSON object followed by a newline.")
                }
                send(response, to: client)
                return
            }
        }
        send(Self.error("request_too_large", "Request exceeds 256 KiB."), to: client)
    }

    private func send(_ response: [String: Any], to client: Int32) {
        guard var data = try? JSONSerialization.data(withJSONObject: response, options: [.sortedKeys]) else { return }
        data.append(10)
        data.withUnsafeBytes { bytes in
            var offset = 0
            while offset < bytes.count {
                let count = Darwin.send(client, bytes.baseAddress!.advanced(by: offset), bytes.count - offset, MSG_NOSIGNAL)
                guard count > 0 else { return }
                offset += count
            }
        }
    }

    static func error(_ code: String, _ message: String) -> [String: Any] {
        ["ok": false, "error": ["code": code, "message": message]]
    }

    private func failure(_ message: String) -> NSError {
        NSError(domain: "BrainControl", code: 1, userInfo: [NSLocalizedDescriptionKey: message])
    }
}
