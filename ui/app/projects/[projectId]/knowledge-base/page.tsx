"use client";

import { MainLayout } from "@/components/layout/main-layout";
import { useLanguage } from "@/providers/LanguageProvider";

function getRagWebuiUrl(): string {
  if (typeof window === "undefined") return "";
  const host = window.location.hostname;
  if (host === "localhost" || host === "127.0.0.1") return "http://localhost:9623/webui";
  return `http://${host}:9623/webui`;
}

export default function KnowledgeBasePage() {
  const { t } = useLanguage();
  const ragUrl = getRagWebuiUrl();

  return (
    <MainLayout title={t("nav.knowledgeBase")}>
      <div className="-m-6 h-full">
        <iframe
          src={ragUrl}
          className="h-full w-full border-0"
          title={t("nav.knowledgeBase")}
          allow="fullscreen"
        />
      </div>
    </MainLayout>
  );
}
