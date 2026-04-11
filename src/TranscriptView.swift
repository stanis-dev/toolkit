import SwiftUI

struct TranscriptView: View {
    let recording: Recording
    @ObservedObject var listState: RecordingListState
    @ObservedObject var appState: AppState
    @ObservedObject var playback: PlaybackState
    @State private var content: String = ""
    @State private var summaryContent: String = ""
    @State private var summaryCollapsed: Bool = false
    @State private var confirmingDelete = false
    @State private var editingTitle = false
    @State private var titleText: String = ""
    @State private var speakers: [String] = []
    @State private var renamingSpeaker: String?
    @State private var renameText: String = ""

    private var txtPath: String { recording.url.path.replacingOccurrences(of: ".wav", with: ".txt") }
    private var polishedPath: String { recording.url.path.replacingOccurrences(of: ".wav", with: ".polished.txt") }
    private var summaryPath: String { recording.url.path.replacingOccurrences(of: ".wav", with: ".summary.md") }
    private var jsonPath: String { recording.url.path.replacingOccurrences(of: ".wav", with: ".json") }

    private func goBack() {
        withAnimation(.easeInOut(duration: 0.2)) { appState.viewingTranscriptId = nil }
    }

    private func loadContent() {
        let path = FileManager.default.fileExists(atPath: polishedPath) ? polishedPath : txtPath
        content = (try? String(contentsOfFile: path, encoding: .utf8)) ?? "Transcript not found."
        summaryContent = (try? String(contentsOfFile: summaryPath, encoding: .utf8)) ?? ""
        var seen = Set<String>()
        var ordered: [String] = []
        for line in content.split(separator: "\n") {
            let s = String(line)
            guard let bracketEnd = s.firstIndex(of: "]"),
                  s[bracketEnd...].contains(":") else { continue }
            let name = s[s.index(after: bracketEnd)...].prefix(while: { $0 != ":" }).trimmingCharacters(in: .whitespaces)
            guard !name.isEmpty else { continue }
            if seen.insert(name).inserted { ordered.append(name) }
        }
        speakers = ordered
    }

    private var reasoningPath: String { recording.url.path.replacingOccurrences(of: ".wav", with: ".reasoning.jsonl") }
    private var summaryReasoningPath: String { recording.url.path.replacingOccurrences(of: ".wav", with: ".summary-reasoning.jsonl") }

    private func deleteTranscript() {
        for path in [txtPath, polishedPath, reasoningPath, summaryPath, summaryReasoningPath, jsonPath] {
            try? FileManager.default.removeItem(atPath: path)
        }
        goBack()
        listState.refresh()
    }

    private func commitTitleEdit() {
        let name = titleText.trimmingCharacters(in: .whitespaces)
        editingTitle = false
        guard !name.isEmpty else { return }
        listState.saveCustomName(id: recording.id, name: name)
    }

    private func commitRename() {
        guard let old = renamingSpeaker else { return }
        let newName = renameText.trimmingCharacters(in: .whitespaces)
        renamingSpeaker = nil
        renameSpeaker(old, to: newName)
    }

    private func renameSpeaker(_ oldName: String, to newName: String) {
        guard !newName.isEmpty, newName != oldName else { return }

        _ = saveSpeakerProfile(oldName: oldName, newName: newName, jsonPath: jsonPath)

        content = content.replacingOccurrences(of: "] \(oldName):", with: "] \(newName):")
        try? content.write(toFile: txtPath, atomically: true, encoding: .utf8)
        speakers = speakers.map { $0 == oldName ? newName : $0 }
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            HStack(spacing: 8) {
                Button(action: goBack) {
                    HStack(spacing: 3) {
                        Image(systemName: "chevron.left")
                            .font(.system(size: 9, weight: .semibold))
                        Text("Back")
                            .font(.system(size: 12, weight: .medium))
                    }
                    .foregroundStyle(.secondary)
                }
                .buttonStyle(NoFocusButtonStyle())

                if editingTitle {
                    HStack(spacing: 4) {
                        TextField("Meeting name", text: $titleText)
                            .textFieldStyle(.plain)
                            .font(.system(size: 12, weight: .medium))
                            .padding(.horizontal, 6)
                            .padding(.vertical, 3)
                            .background(.quaternary, in: RoundedRectangle(cornerRadius: 4))
                            .onSubmit { commitTitleEdit() }
                        Button(action: { commitTitleEdit() }) {
                            Image(systemName: "checkmark")
                                .font(.system(size: 9, weight: .bold))
                                .foregroundStyle(.green)
                        }
                        .buttonStyle(NoFocusButtonStyle())
                        Button(action: { editingTitle = false }) {
                            Image(systemName: "xmark")
                                .font(.system(size: 9, weight: .bold))
                                .foregroundStyle(.secondary)
                        }
                        .buttonStyle(NoFocusButtonStyle())
                    }
                } else {
                    Button(action: {
                        titleText = recording.customName ?? ""
                        editingTitle = true
                    }) {
                        HStack(spacing: 4) {
                            Text(recording.displayName)
                                .font(.system(size: 12, weight: .medium))
                            Image(systemName: "pencil")
                                .font(.system(size: 9))
                                .foregroundStyle(.tertiary)
                        }
                    }
                    .buttonStyle(NoFocusButtonStyle())
                }

                Spacer()

                if confirmingDelete {
                    Text("Delete transcript?")
                        .font(.system(size: 11, weight: .medium))
                        .foregroundStyle(.secondary)
                    Button(action: {
                        deleteTranscript()
                        withAnimation { confirmingDelete = false }
                    }) {
                        Image(systemName: "checkmark")
                            .font(.system(size: 11, weight: .bold))
                            .foregroundStyle(.green)
                    }
                    .buttonStyle(NoFocusButtonStyle())
                    Button(action: { withAnimation { confirmingDelete = false } }) {
                        Image(systemName: "xmark")
                            .font(.system(size: 11, weight: .bold))
                            .foregroundStyle(.red)
                    }
                    .buttonStyle(NoFocusButtonStyle())
                } else {
                    HoverIconButton("arrow.counterclockwise") {
                        listState.transcribe(id: recording.id); goBack()
                    }
                    HoverIconButton("trash") { withAnimation { confirmingDelete = true } }
                }
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 6)

            if !speakers.isEmpty {
                Divider().padding(.horizontal, 8)
                HStack(spacing: 6) {
                    ForEach(Array(speakers.enumerated()), id: \.offset) { _, speaker in
                        if renamingSpeaker == speaker {
                            HStack(spacing: 4) {
                                TextField("Name", text: $renameText)
                                    .textFieldStyle(.plain)
                                    .font(.system(size: 11))
                                    .frame(width: 80)
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 3)
                                    .background(.quaternary, in: RoundedRectangle(cornerRadius: 4))
                                    .onSubmit { commitRename() }
                                Button(action: { commitRename() }) {
                                    Image(systemName: "checkmark")
                                        .font(.system(size: 9, weight: .bold))
                                        .foregroundStyle(.green)
                                }
                                .buttonStyle(NoFocusButtonStyle())
                                Button(action: { renamingSpeaker = nil }) {
                                    Image(systemName: "xmark")
                                        .font(.system(size: 9, weight: .bold))
                                        .foregroundStyle(.secondary)
                                }
                                .buttonStyle(NoFocusButtonStyle())
                            }
                        } else {
                            Button(action: {
                                renameText = speaker
                                renamingSpeaker = speaker
                            }) {
                                Text(speaker)
                                    .font(.system(size: 11, weight: .medium))
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 3)
                                    .background(.quaternary, in: RoundedRectangle(cornerRadius: 4))
                            }
                            .buttonStyle(NoFocusButtonStyle())
                        }
                    }
                    Spacer()
                }
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
            }

            Divider().padding(.horizontal, 8)

            if !summaryContent.isEmpty {
                VStack(alignment: .leading, spacing: 0) {
                    Button(action: { withAnimation(.easeInOut(duration: 0.2)) { summaryCollapsed.toggle() } }) {
                        HStack(spacing: 6) {
                            Image(systemName: summaryCollapsed ? "chevron.right" : "chevron.down")
                                .font(.system(size: 9, weight: .semibold))
                                .foregroundStyle(.secondary)
                            Text("Summary & To-Dos")
                                .font(.system(size: 12, weight: .medium))
                                .foregroundStyle(.primary)
                            Spacer()
                        }
                        .padding(.horizontal, 12)
                        .padding(.vertical, 6)
                        .contentShape(Rectangle())
                    }
                    .buttonStyle(NoFocusButtonStyle())

                    if !summaryCollapsed {
                        ScrollView {
                            if let attributed = try? AttributedString(
                                markdown: summaryContent,
                                options: .init(interpretedSyntax: .inlineOnlyPreservingWhitespace)
                            ) {
                                Text(attributed)
                                    .font(.system(size: 12))
                                    .textSelection(.enabled)
                                    .frame(maxWidth: .infinity, alignment: .leading)
                                    .padding(.horizontal, 12)
                                    .padding(.bottom, 8)
                            } else {
                                Text(summaryContent)
                                    .font(.system(size: 12))
                                    .textSelection(.enabled)
                                    .frame(maxWidth: .infinity, alignment: .leading)
                                    .padding(.horizontal, 12)
                                    .padding(.bottom, 8)
                            }
                        }
                        .frame(maxHeight: 200)
                    }
                }
                .background(.background.opacity(0.5))

                Divider().padding(.horizontal, 8)
            }

            ScrollView {
                LazyVStack(alignment: .leading, spacing: 2) {
                    ForEach(Array(contentLines.enumerated()), id: \.offset) { _, line in
                        if let (ts, seconds, rest) = parseTimestampLine(line) {
                            HStack(alignment: .firstTextBaseline, spacing: 0) {
                                Button(action: { playback.playFrom(recording: recording, time: seconds) }) {
                                    Text(ts)
                                        .font(.system(size: 12, design: .monospaced))
                                        .foregroundStyle(Color.accentColor)
                                }
                                .buttonStyle(NoFocusButtonStyle())
                                .help("Play from \(ts)")

                                if let attributed = try? AttributedString(
                                    markdown: rest,
                                    options: .init(interpretedSyntax: .inlineOnlyPreservingWhitespace)
                                ) {
                                    Text(attributed)
                                        .font(.system(size: 13))
                                        .textSelection(.enabled)
                                } else {
                                    Text(rest)
                                        .font(.system(size: 13))
                                        .textSelection(.enabled)
                                }
                            }
                            .padding(.horizontal, 12)
                            .padding(.top, 6)
                        } else if !line.isEmpty {
                            if let attributed = try? AttributedString(
                                markdown: line,
                                options: .init(interpretedSyntax: .inlineOnlyPreservingWhitespace)
                            ) {
                                Text(attributed)
                                    .font(.system(size: 13))
                                    .textSelection(.enabled)
                                    .padding(.horizontal, 12)
                            } else {
                                Text(line)
                                    .font(.system(size: 13))
                                    .textSelection(.enabled)
                                    .padding(.horizontal, 12)
                            }
                        }
                    }
                }
                .padding(.vertical, 8)
            }

            if playback.playingId == recording.id {
                Divider()
                HStack(spacing: 8) {
                    Button(action: { playback.toggle(recording: recording) }) {
                        Image(systemName: playback.isPlaying ? "pause.fill" : "play.fill")
                            .font(.system(size: 11))
                            .foregroundStyle(.primary)
                    }
                    .buttonStyle(NoFocusButtonStyle())

                    Text(formatDuration(playback.currentTime))
                        .font(.system(size: 11, design: .monospaced))
                        .foregroundStyle(.secondary)

                    GeometryReader { geo in
                        ZStack(alignment: .leading) {
                            Rectangle().fill(.quaternary).frame(height: 3)
                            Rectangle().fill(Color.accentColor)
                                .frame(width: geo.size.width * playback.progress, height: 3)
                        }
                        .cornerRadius(1.5)
                        .frame(height: geo.size.height)
                        .contentShape(Rectangle())
                        .gesture(DragGesture(minimumDistance: 0).onChanged { v in
                            playback.seek(to: max(0, min(1, v.location.x / geo.size.width)))
                        })
                    }
                    .frame(height: 16)

                    Button(action: { playback.stop() }) {
                        Image(systemName: "xmark")
                            .font(.system(size: 9, weight: .bold))
                            .foregroundStyle(.secondary)
                    }
                    .buttonStyle(NoFocusButtonStyle())
                }
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .contentShape(Rectangle())
        .onTapGesture {
            if confirmingDelete { withAnimation { confirmingDelete = false } }
        }
        .onAppear { loadContent() }
    }

    private var contentLines: [String] {
        content.split(separator: "\n", omittingEmptySubsequences: false).map(String.init)
    }

    private func parseTimestampLine(_ line: String) -> (String, TimeInterval, String)? {
        guard line.hasPrefix("[") else { return nil }
        guard let closeBracket = line.firstIndex(of: "]") else { return nil }
        let ts = String(line[line.startIndex...closeBracket])
        let inner = String(line[line.index(after: line.startIndex)..<closeBracket])
        let parts = inner.split(separator: ":").compactMap { Double($0) }
        var seconds: TimeInterval = 0
        if parts.count == 3 { seconds = parts[0] * 3600 + parts[1] * 60 + parts[2] }
        else if parts.count == 2 { seconds = parts[0] * 60 + parts[1] }
        else { return nil }
        let rest = String(line[line.index(after: closeBracket)...])
        return (ts, seconds, rest)
    }
}

func saveSpeakerProfile(oldName: String, newName: String, jsonPath: String) -> Bool {
    guard let jsonData = FileManager.default.contents(atPath: jsonPath),
          let json = try? JSONSerialization.jsonObject(with: jsonData) as? [String: Any],
          let embeddings = json["speaker_embeddings"] as? [String: [Double]],
          let embedding = embeddings[oldName]
    else { return false }

    var profiles: [String: Any] = [:]
    if let existing = FileManager.default.contents(atPath: kSpeakersFile),
       let parsed = try? JSONSerialization.jsonObject(with: existing) as? [String: Any] {
        profiles = parsed
    }

    if let old = profiles[oldName] as? [String: Any], old["embedding"] != nil {
        profiles.removeValue(forKey: oldName)
    }

    if let existing = profiles[newName] as? [String: Any],
       let stored = existing["embedding"] as? [Double] {
        let averaged = zip(stored, embedding).map { ($0 + $1) / 2.0 }
        profiles[newName] = ["embedding": averaged]
    } else {
        profiles[newName] = ["embedding": embedding]
    }

    guard let out = try? JSONSerialization.data(withJSONObject: profiles, options: [.prettyPrinted, .sortedKeys]) else { return false }
    return FileManager.default.createFile(atPath: kSpeakersFile, contents: out)
}
