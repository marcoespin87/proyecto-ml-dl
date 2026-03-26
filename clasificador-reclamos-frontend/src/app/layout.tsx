import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Clasificador de Reclamos",
  description: "Sistema de clasificacion automatica de reclamos de consumidores",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
