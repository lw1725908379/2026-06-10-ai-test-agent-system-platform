"use client";

import { MainLayout } from "@/components/layout/main-layout";
import { useLanguage } from "@/providers/LanguageProvider";

export default function KnowledgeBasePage() {
  const { t } = useLanguage();

  return (
    <MainLayout title={t("nav.knowledgeBase")}>
      <div className="-m-6 h-full">
        <iframe
          src="http://localhost:9623/webui"
          className="h-full w-full border-0"
          title={t("nav.knowledgeBase")}
          allow="fullscreen"
        />
      </div>
    </MainLayout>
  );
}
