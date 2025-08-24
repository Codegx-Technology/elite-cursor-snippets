import Welcome from "@/components/Welcome";
import { useTranslations } from "next-intl";

export default function Home() {
  const t = useTranslations("Index");
  return <Welcome title={t("title")} />;
}
