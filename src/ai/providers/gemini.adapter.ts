import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { ProviderAdapter } from "./base.adapter";
import { ProviderIdentifier, TaskType } from "../registry/registry.types";

const pExecFile = promisify(execFile);

// Minimal mapping: extend as needed
const SUPPORTED: TaskType[] = ["text-generation", "text-summarization"];

export const GeminiAdapter: ProviderAdapter = {
  name: "gemini",
  supports(task: TaskType) {
    return SUPPORTED.includes(task);
  },
  async execute(task, id: ProviderIdentifier, payload) {
    if (!id.modelId) {
      return { ok: false, error: new Error("Missing Gemini modelId"), provider: "gemini" };
    }
    try {
      // Example: gemini text -m gemini-1.5-pro "your prompt"
      const args = ["text", "-m", id.modelId, payload.prompt ?? ""];
      const { stdout, stderr } = await pExecFile("gemini", args, { timeout: 180000 });
      if (stderr && stderr.trim().length > 0) {
        // Gemini CLI often prints warnings to stderr; treat only critical as error if needed
      }
      return {
        ok: true,
        data: stdout?.trim(),
        provider: "gemini",
        modelId: id.modelId
      };
    } catch (e: any) {
      return { ok: false, error: e, provider: "gemini", modelId: id.modelId };
    }
  }
};
