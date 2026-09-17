import Foundation

@main
struct ControlTestHost {
    static func main() {
        let server = ControlServer(path: CommandLine.arguments[1]) { request in
            if request["command"] as? String == "echo" { return ["ok": true, "result": request] }
            return ControlServer.error("unknown_command", "Unknown command.")
        }
        do { try server.start() }
        catch { fputs("\(error.localizedDescription)\n", stderr); exit(1) }
        withExtendedLifetime(server) { dispatchMain() }
    }
}
