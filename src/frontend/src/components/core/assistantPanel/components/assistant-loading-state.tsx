import {
  ArrowRight,
  Check,
  ChevronDown,
  ChevronRight,
  Code2,
} from "lucide-react";
import { memo, useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import type { AgenticProgressState } from "@/controllers/API/queries/agentic";
import { GHOST_PRIMARY_BUTTON } from "../helpers/button-styles";

interface AssistantLoadingStateProps {
  progress: AgenticProgressState;
  streamingContent?: string;
  onValidationComplete?: () => void;
}

// Flow-build steps that have no body content (no streaming code, no card).
// For those, the bordered card looks like an "empty" loading box, so we swap
// it for a minimal draw-on animation of the Intugle icon glyph.
const FLOW_BUILD_ICON_STEPS = new Set([
  "searching_components",
  "generating_plan",
  "generating_flow",
  "generating_document",
  "orchestrating",
  "building_flow",
  "flow_built",
]);

// SVG `d` of the six wavy strokes that form the Intugle icon glyph, in a
// 100x100 viewBox. Each stroke is its own sub-path (`d` string).
const INTUGLE_ICON_PATHS: readonly string[] = [
  "M34.5739 55.9804C34.8338 56.936 37.6656 66.7522 47.6645 70.4412C54.7825 73.0692 62.8561 71.5866 68.7515 66.6047",
  "M77.2326 70.0969C75.7851 71.9519 71.014 77.5943 62.4767 79.878C54.0798 82.1265 47.2288 79.7375 45.0225 78.8662",
  "M89.993 25.5128C80.7459 12.3379 65.0203 5.3253 49.2384 7.3419C32.1988 9.5131 18.3493 21.7887 13.7117 37.4089C7.71091 57.6176 17.8574 80.9882 38.3612 89.4413C56.518 96.932 78.0547 90.7553 90 74.3129",
  "M76.7547 28.2884C64.4862 16.1252 45.2894 15.802 33.8289 26.0328C20.9982 37.4792 20.5204 59.7959 34.9883 72.8584",
  "M57.8811 37.8165C52.3301 36.7484 46.8493 39.2007 44.411 43.6345C41.3896 49.1364 43.4976 56.8657 49.8075 60.4985",
  "M38.9514 36.4252C40.0054 34.9847 43.5539 30.5017 50.0605 28.6537C57.5931 26.5176 63.7485 29.4407 65.1608 30.1574",
];

// Animation tuning constants.
// All strokes are normalized to the same length via `pathLength`, so every
// sub-path animates in lock-step regardless of its real geometry.
const PATH_LENGTH = 100;
// Duration of one full draw-fade cycle.
const DRAW_DURATION_SECONDS = 2.4;
// Keyframe percentages for the fill-up + hold + fade loop:
//   start       — fully undrawn, invisible (let the gray base show through)
//   fade-in     — pink stroke becomes visible while still undrawn
//   filled      — stroke fully drawn over the gray base
//   hold filled — pause so "complete" reads
//   end         — fades out; offset resets to start invisibly on the next loop
const KEYFRAME_FADE_IN_PERCENT = 8;
const KEYFRAME_FILLED_PERCENT = 65;
const KEYFRAME_HOLD_END_PERCENT = 85;

function LangflowDrawingIcon({ size = 24 }: { size?: number }) {
  const animationName = "intugle-assistant-fill";

  return (
    <span
      className="inline-flex shrink-0 items-center"
      data-testid="assistant-flow-loading-icon"
      role="status"
      aria-label="Generating flow"
    >
      <svg
        width={size}
        height={size}
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <linearGradient
            id="intugle-assistant-gradient"
            x1="52"
            y1="5"
            x2="52"
            y2="95"
            gradientUnits="userSpaceOnUse"
          >
            <stop stopColor="#7AB5FC" />
            <stop offset="0.5" stopColor="#3073F0" />
            <stop offset="1" stopColor="#1E3D9C" />
          </linearGradient>
        </defs>
        {INTUGLE_ICON_PATHS.map((d, index) => (
          <path
            key={`base-${index}`}
            d={d}
            stroke="currentColor"
            strokeOpacity="0.18"
            strokeWidth="5"
            strokeMiterlimit="10"
            strokeLinecap="round"
            className="text-muted-foreground"
          />
        ))}
        {INTUGLE_ICON_PATHS.map((d, index) => (
          <path
            key={`draw-${index}`}
            d={d}
            stroke="url(#intugle-assistant-gradient)"
            strokeWidth="5"
            strokeMiterlimit="10"
            strokeLinecap="round"
            pathLength={PATH_LENGTH}
            style={{
              strokeDasharray: PATH_LENGTH,
              strokeDashoffset: PATH_LENGTH,
              opacity: 0,
              animation: `${animationName} ${DRAW_DURATION_SECONDS}s ease-out infinite`,
            }}
          />
        ))}
      </svg>
      <style>{`
        @keyframes ${animationName} {
          0%                                  { stroke-dashoffset: ${PATH_LENGTH}; opacity: 0; }
          ${KEYFRAME_FADE_IN_PERCENT}%       { opacity: 1; }
          ${KEYFRAME_FILLED_PERCENT}%        { stroke-dashoffset: 0; opacity: 1; }
          ${KEYFRAME_HOLD_END_PERCENT}%      { stroke-dashoffset: 0; opacity: 1; }
          100%                                { stroke-dashoffset: 0; opacity: 0; }
        }
      `}</style>
    </span>
  );
}

function AssistantLoadingStateComponent({
  progress,
  streamingContent,
  onValidationComplete,
}: AssistantLoadingStateProps) {
  const { t } = useTranslation();
  const [codeOpen, setCodeOpen] = useState(true);
  const streamingRef = useRef<HTMLPreElement>(null);

  const isValidated = progress.step === "validated";
  const isReady = isValidated && !!progress.componentCode;
  const finalCode = progress.componentCode;
  const hasStreaming = !!streamingContent && streamingContent.length > 0;
  const showStreamingPreview = !finalCode && hasStreaming;

  // Auto-scroll streaming preview
  useEffect(() => {
    if (streamingRef.current) {
      streamingRef.current.scrollTop = streamingRef.current.scrollHeight;
    }
  }, [streamingContent]);

  // Minimal icon-only mode: flow-build steps with no body content. Swaps the
  // bordered card (which would render essentially empty) for a draw-on Langflow
  // glyph animation. Must come AFTER all hook calls to preserve hook order.
  const isFlowBuildIconMode =
    FLOW_BUILD_ICON_STEPS.has(progress.step) &&
    !hasStreaming &&
    !finalCode &&
    !progress.error;

  if (isFlowBuildIconMode) {
    return (
      <div
        data-testid="assistant-flow-loading-icon-mode"
        className="flex items-center gap-2 text-sm font-medium text-foreground"
      >
        <LangflowDrawingIcon size={24} />
        <span>{progress.message || "Working..."}</span>
      </div>
    );
  }

  return (
    <div className="w-full max-w-[600px] py-1">
      {/* Header — status line, flat (no surrounding card). Uses the same
          LangflowDrawingIcon (size 24) as the flow-build minimal mode so the
          loading glyph is visually identical across component generation and
          flow building. */}
      <div className="mb-2 flex items-center gap-2 text-sm font-medium">
        {isReady ? (
          <Check className="h-4 w-4 text-accent-emerald-foreground" />
        ) : (
          <LangflowDrawingIcon size={24} />
        )}
        <span
          className={
            isReady ? "text-accent-emerald-foreground" : "text-foreground"
          }
        >
          {isReady
            ? t("assistant.componentReady")
            : progress.message || t("assistant.working")}
        </span>
        {progress.className && (
          <span className="ml-auto font-mono text-[11px] text-muted-foreground/80">
            {progress.className}
          </span>
        )}
      </div>

      {/* Live streaming — the main content while LLM generates */}
      {showStreamingPreview && (
        <pre
          ref={streamingRef}
          className="custom-scroll mb-2 max-h-[300px] overflow-auto rounded-md bg-muted/30 px-3 py-2 text-xs leading-relaxed"
        >
          <code className="whitespace-pre-wrap">{streamingContent}</code>
        </pre>
      )}

      {/* Validation error */}
      {progress.error && (
        <div className="mb-2 w-fit rounded-md bg-destructive/10 px-2.5 py-1.5 text-xs text-destructive">
          {progress.error}
        </div>
      )}

      {/* Retry counter */}
      {progress.attempt > 1 && (
        <div className="mb-2 text-xs text-muted-foreground">
          {t("assistant.attempt", {
            attempt: progress.attempt,
            max: progress.maxAttempts,
          })}
        </div>
      )}

      {/* Final extracted code — replaces streaming preview */}
      {finalCode && (
        <div className="mb-2">
          <button
            type="button"
            onClick={() => setCodeOpen((prev) => !prev)}
            className="flex items-center gap-1.5 text-xs text-muted-foreground transition-colors hover:text-foreground"
          >
            {codeOpen ? (
              <ChevronDown className="h-3 w-3" />
            ) : (
              <ChevronRight className="h-3 w-3" />
            )}
            <Code2 className="h-3 w-3" />
            <span>{t("assistant.code")}</span>
          </button>
          {codeOpen && (
            <pre className="custom-scroll mt-2 max-h-[180px] overflow-auto rounded-md bg-muted/30 px-3 py-2 text-xs leading-relaxed">
              <code>{finalCode}</code>
            </pre>
          )}
        </div>
      )}

      {/* Continue — same ghost style as the plan card / component result. */}
      {isReady && (
        <button
          type="button"
          data-testid="assistant-continue-button"
          onClick={() => onValidationComplete?.()}
          className={GHOST_PRIMARY_BUTTON}
        >
          <span>{t("assistant.continue")}</span>
          <ArrowRight className="h-3.5 w-3.5" />
        </button>
      )}
    </div>
  );
}

export const AssistantLoadingState = memo(AssistantLoadingStateComponent);
export default AssistantLoadingState;
