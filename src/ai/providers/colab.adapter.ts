import { ProviderAdapter } from "./base.adapter";
import { ProviderIdentifier, TaskType } from "../registry/registry.types";

const SUPPORTED: TaskType[] = [
  "image-generation",
  "audio-transcription",
  "text-generation",
  "text-summarization"
];

export const ColabAdapter: ProviderAdapter = {
  name: "colab",
  supports(task) {
    return SUPPORTED.includes(task);
  },
  async execute(task, id: ProviderIdentifier, payload) {
    try {
      const base =
        "https://colab.research.google.com/github/your-org/your-repo/blob/main/notebooks/colab/runner.ipynb";
      const q = new URLSearchParams({
        task,
        modelId: id.modelId ?? "",
        prompt: (payload.prompt ?? "").toString()
      }).toString();
      const url = `${base}?${q}`;
      return {
        ok: true,
        data: { action: "open_url", url },
        provider: "colab",
        modelId: id.modelId
      };
    } catch (e: any) {
      return { ok: false, error: e, provider: "colab", modelId: id.modelId };
    }
  }
};
