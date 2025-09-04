import Layout from "@/components/Layout";

export default function VideoGenerateLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <Layout>{children}</Layout>;
}
