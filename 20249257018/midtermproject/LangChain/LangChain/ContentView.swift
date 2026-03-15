//
//  ContentView.swift
//  LangChain
//
//  Created by Ahmet Buğra Özcan on 16.03.2026.
//

import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = CodeReviewViewModel()
    private let canvasColor = Color(red: 0.95, green: 0.96, blue: 0.98)
    private let panelColor = Color.white
    private let panelBorder = Color(red: 0.84, green: 0.87, blue: 0.91)
    private let titleColor = Color(red: 0.11, green: 0.14, blue: 0.20)
    private let bodyColor = Color(red: 0.20, green: 0.24, blue: 0.31)
    private let mutedColor = Color(red: 0.39, green: 0.44, blue: 0.53)

    var body: some View {
        ScrollView {
            VStack(spacing: 16) {
                header

                HSplitView {
                    codeEditorPanel
                    resultsPanel
                }
                .frame(minHeight: 360)

                agentPanel
            }
            .padding(20)
            .frame(maxWidth: .infinity, alignment: .topLeading)
        }
        .background(canvasColor)
        .frame(minWidth: 1180, minHeight: 820)
        .preferredColorScheme(.light)
        .task {
            if viewModel.review == nil && !viewModel.sourceCode.isEmpty {
                await viewModel.analyze()
            }
        }
    }

    private var header: some View {
        HStack {
            VStack(alignment: .leading, spacing: 6) {
                Text("Autonomous Swift Review")
                    .font(.largeTitle.bold())
                    .foregroundStyle(titleColor)
                Text("Phase 1: structured code review, Phase 2: self-healing build loop")
                    .foregroundStyle(mutedColor)
            }
            Spacer()
            statusBadge(title: "Audit", detail: viewModel.analyzeStatus, isActive: viewModel.isAnalyzing)
            statusBadge(title: "Agent", detail: viewModel.healingStatus, isActive: viewModel.isHealing)
            Button("Analyze Code") {
                Task { await viewModel.analyze() }
            }
            .disabled(viewModel.isAnalyzing || viewModel.sourceCode.isEmpty)

            Button("Run Self-Healing Agent") {
                Task { await viewModel.startSelfHealing() }
            }
            .buttonStyle(.borderedProminent)
            .disabled(viewModel.isHealing || viewModel.sourceCode.isEmpty)
        }
    }

    private func statusBadge(title: String, detail: String, isActive: Bool) -> some View {
        VStack(alignment: .leading, spacing: 3) {
            HStack(spacing: 6) {
                Circle()
                    .fill(isActive ? Color(red: 0.15, green: 0.56, blue: 0.38) : Color(red: 0.63, green: 0.67, blue: 0.74))
                    .frame(width: 8, height: 8)
                Text(title)
                    .font(.caption.weight(.semibold))
                    .foregroundStyle(titleColor)
            }
            Text(detail)
                .font(.caption)
                .foregroundStyle(mutedColor)
                .lineLimit(2)
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 10)
        .background(panelColor, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
        .overlay(
            RoundedRectangle(cornerRadius: 14, style: .continuous)
                .stroke(panelBorder, lineWidth: 1)
        )
        .frame(width: 220, alignment: .leading)
    }

    private var codeEditorPanel: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("Swift Code Input")
                    .font(.title3.weight(.semibold))
                    .foregroundStyle(titleColor)
                Spacer()
                if viewModel.isAnalyzing {
                    ProgressView()
                        .controlSize(.small)
                        .tint(Color(red: 0.17, green: 0.42, blue: 0.82))
                }
            }
            TextEditor(text: $viewModel.sourceCode)
                .font(.system(.body, design: .monospaced))
                .foregroundStyle(bodyColor)
                .scrollContentBackground(.hidden)
                .padding(12)
                .background(panelColor, in: RoundedRectangle(cornerRadius: 18, style: .continuous))
                .overlay(
                    RoundedRectangle(cornerRadius: 18, style: .continuous)
                        .stroke(panelBorder, lineWidth: 1)
                )
        }
        .padding(18)
        .background(panelColor, in: RoundedRectangle(cornerRadius: 24, style: .continuous))
        .overlay(
            RoundedRectangle(cornerRadius: 24, style: .continuous)
                .stroke(panelBorder, lineWidth: 1)
        )
    }

    private var resultsPanel: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("Structured Review")
                    .font(.title3.weight(.semibold))
                    .foregroundStyle(titleColor)
                Spacer()
                if viewModel.isAnalyzing {
                    ProgressView("Auditing...")
                        .controlSize(.small)
                        .tint(Color(red: 0.17, green: 0.42, blue: 0.82))
                }
            }

            if let review = viewModel.review {
                VStack(alignment: .leading, spacing: 12) {
                    Label("Score: \(review.score)/100", systemImage: "checklist")
                        .font(.headline)
                        .foregroundStyle(titleColor)

                    List(review.issues) { issue in
                        VStack(alignment: .leading, spacing: 8) {
                            HStack {
                                Text("Line \(issue.line)")
                                    .font(.headline)
                                    .foregroundStyle(titleColor)
                                Spacer()
                                Text(severityText(for: issue).uppercased())
                                    .font(.caption.weight(.bold))
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 4)
                                    .background(severityColor(for: issue).opacity(0.15))
                                    .foregroundStyle(severityColor(for: issue))
                                    .clipShape(Capsule())
                            }
                            Text(issue.message)
                                .foregroundStyle(Color(red: 0.20, green: 0.24, blue: 0.31))
                            Text(issue.suggestion)
                                .foregroundStyle(Color(red: 0.35, green: 0.41, blue: 0.50))
                        }
                        .padding(14)
                        .background(panelColor, in: RoundedRectangle(cornerRadius: 16, style: .continuous))
                        .overlay(
                            RoundedRectangle(cornerRadius: 16, style: .continuous)
                                .stroke(severityColor(for: issue).opacity(0.22), lineWidth: 1)
                        )
                        .listRowBackground(Color.clear)
                    }
                    .listStyle(.plain)
                    .scrollContentBackground(.hidden)
                }
            } else if viewModel.isAnalyzing {
                VStack(alignment: .leading, spacing: 12) {
                    ProgressView()
                        .tint(Color(red: 0.17, green: 0.42, blue: 0.82))
                    Text("Running strict Swift audit and building structured findings...")
                        .foregroundStyle(mutedColor)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .center)
            } else {
                ContentUnavailableView("No Review Yet", systemImage: "doc.text.magnifyingglass")
                    .foregroundStyle(titleColor, mutedColor)
            }

            if let errorMessage = viewModel.errorMessage {
                Text(errorMessage)
                    .foregroundStyle(.red)
            }
        }
        .padding(18)
        .background(panelColor, in: RoundedRectangle(cornerRadius: 24, style: .continuous))
        .overlay(
            RoundedRectangle(cornerRadius: 24, style: .continuous)
                .stroke(panelBorder, lineWidth: 1)
        )
    }

    private var agentPanel: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("Agent Dashboard")
                    .font(.title3.weight(.semibold))
                    .foregroundStyle(titleColor)
                Spacer()
                if viewModel.isHealing {
                    ProgressView("Running...")
                        .controlSize(.small)
                        .tint(Color(red: 0.18, green: 0.53, blue: 0.35))
                }
            }

            HSplitView {
                VStack(alignment: .leading, spacing: 8) {
                    Text("Thought / Action Log")
                        .font(.headline)
                        .foregroundStyle(titleColor)
                    List(viewModel.logs) { log in
                        VStack(alignment: .leading, spacing: 6) {
                            Text(log.title)
                                .font(.headline)
                                .foregroundStyle(titleColor)
                            Text(log.detail)
                                .font(.system(.body, design: .monospaced))
                                .textSelection(.enabled)
                                .foregroundStyle(Color(red: 0.19, green: 0.22, blue: 0.30))
                        }
                        .padding(12)
                        .background(color(for: log.level).opacity(0.10), in: RoundedRectangle(cornerRadius: 14, style: .continuous))
                        .overlay(
                            RoundedRectangle(cornerRadius: 14, style: .continuous)
                                .stroke(color(for: log.level).opacity(0.18), lineWidth: 1)
                        )
                        .listRowBackground(Color.clear)
                    }
                    .listStyle(.plain)
                    .scrollContentBackground(.hidden)
                }

                VStack(alignment: .leading, spacing: 8) {
                    Text("Original / Final Diff")
                        .font(.headline)
                        .foregroundStyle(titleColor)
                    HStack(spacing: 12) {
                        CodeBlockView(title: "Original", code: viewModel.sourceCode)
                        CodeBlockView(
                            title: "Final",
                            code: viewModel.finalCode,
                            placeholder: viewModel.isHealing
                                ? "// Waiting for the agent to produce a compilable revision..."
                                : "// Run the self-healing workflow to render the final Swift output."
                        )
                    }
                }
            }
            .frame(minHeight: 280, idealHeight: 320)

            summaryPanel
        }
        .padding(18)
        .background(panelColor, in: RoundedRectangle(cornerRadius: 24, style: .continuous))
        .overlay(
            RoundedRectangle(cornerRadius: 24, style: .continuous)
                .stroke(panelBorder, lineWidth: 1)
        )
    }

    private var summaryPanel: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Backend Summary")
                .font(.headline)
                .foregroundStyle(titleColor)

            if viewModel.isHealing && viewModel.healingSummary.isEmpty {
                VStack(alignment: .leading, spacing: 10) {
                    ProgressView()
                        .tint(Color(red: 0.18, green: 0.53, blue: 0.35))
                    Text("Collecting and summarizing backend changes...")
                        .foregroundStyle(mutedColor)
                }
            } else if viewModel.healingSummary.isEmpty {
                Text("No summary yet. Run the self-healing workflow to see what changed.")
                    .foregroundStyle(mutedColor)
            } else {
                ForEach(Array(viewModel.healingSummary.enumerated()), id: \.offset) { index, item in
                    HStack(alignment: .top, spacing: 10) {
                        Text("\(index + 1).")
                            .font(.system(.body, design: .monospaced))
                            .foregroundStyle(Color(red: 0.27, green: 0.35, blue: 0.56))
                        Text(item)
                            .foregroundStyle(Color(red: 0.19, green: 0.22, blue: 0.30))
                            .frame(maxWidth: .infinity, alignment: .leading)
                    }
                    .padding(12)
                    .background(Color(red: 0.95, green: 0.97, blue: 0.99), in: RoundedRectangle(cornerRadius: 14, style: .continuous))
                    .overlay(
                        RoundedRectangle(cornerRadius: 14, style: .continuous)
                            .stroke(Color(red: 0.84, green: 0.87, blue: 0.91), lineWidth: 1)
                    )
                }
            }
        }
    }

    private func color(for level: DashboardLog.Level) -> Color {
        switch level {
        case .info:
            return .blue
        case .success:
            return .green
        case .failure:
            return .red
        }
    }

    private func severityText(for issue: CodeIssue) -> String {
        issue.message.localizedCaseInsensitiveContains("error") ? "error" : "warning"
    }

    private func severityColor(for issue: CodeIssue) -> Color {
        issue.message.localizedCaseInsensitiveContains("error") ? .red : .orange
    }
}

#Preview {
    ContentView()
}
