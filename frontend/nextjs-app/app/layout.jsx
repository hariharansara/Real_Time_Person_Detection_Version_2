export const metadata = {
  title: "Person Identification AI",
  description: "Real-time face recognition system",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, padding: 0 }}>{children}</body>
    </html>
  );
}
