import { ProviderAdapter } from "./base.adapter";
import { ProviderIdentifier, TaskType } from "../registry/registry.types";
import { exec } from "node:child_process";
import { promisify } from "node:util";

const pExec = promisify(exec);

const SUPPORTED: TaskType[] = [
  "image-generation",
  "audio-transcription",
  "text-generation",
  "text-summarization"
];

export const KaggleAdapter: ProviderAdapter = {
  name: "kaggle",
  supports(task) {
    return SUPPORTED.includes(task);
  },
  async execute(task, id: ProviderIdentifier, payload) {
    try {
      // Placeholder: assumes a prepared kernel project under notebooks/kaggle
      // In production, parameterize via env/metadata files
      await pExec(`kaggle kernels push -p notebooks/kaggle`, { timeout: 300000 });
      // TODO: capture kernel ID or use deterministic slug; then fetch outputs
      // const { stdout } = await pExec(`kaggle kernels output <owner>/<slug> -p ./outputs`);
      return {
        ok: true,
        data: { message: "Kaggle job initiated. Poll outputs endpoint.", task, modelId: id.modelId },
        provider: "kaggle",
        modelId: id.modelId
      };
    } catch (e: any) {
      return { ok: false, error: e, provider: "kaggle", modelId: id.modelId };
    }
  }
};
