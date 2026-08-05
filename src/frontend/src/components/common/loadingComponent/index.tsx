import { useTranslation } from "react-i18next";
import IntugleIcon from "@/assets/IntugleIcon.svg?react";
import type { LoadingComponentProps } from "../../../types/components";

export default function LoadingComponent({
  remSize,
}: LoadingComponentProps): JSX.Element {
  const { t } = useTranslation();
  return (
    <div role="status" className="flex flex-col items-center justify-center">
      <IntugleIcon
        aria-hidden="true"
        title={t("common.intugleLogo")}
        className="animate-pulse text-primary"
        style={{
          width: `${remSize * 0.25}rem`,
          height: `${remSize * 0.25}rem`,
        }}
      />
      <br></br>
      <span className="animate-pulse text-lg text-primary">
        {t("loading.loading")}
      </span>
    </div>
  );
}
