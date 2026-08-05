import type { FlowType } from "@/types/flow";
import { addVersionToDuplicates } from "@/utils/reactflowUtils";

// Flow names are user-scoped in the backend (`unique_flow_name` on
// `(user_id, name)`), so client-side dedupe must mirror that rule.
export function getFolderScopedDuplicateName(
  flow: FlowType,
  flows: FlowType[],
  _folderId?: string | null,
): string {
  return addVersionToDuplicates(flow, flows);
}
