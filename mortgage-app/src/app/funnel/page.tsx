import LeadFunnel from "@/components/LeadFunnel";

export default function FunnelPage() {
  return (
    <main style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'hsl(var(--background))' }}>
      {/* Background Decor - Refined for Navy Night */}
      <div style={{
        position: 'fixed',
        top: '15%',
        right: '-5%',
        width: '45%',
        height: '65%',
        background: 'hsla(var(--nh-gold), 0.08)',
        filter: 'blur(150px)',
        borderRadius: '100%',
        zIndex: 0
      }} />

      <div style={{ zIndex: 1, width: '100%' }}>
        <LeadFunnel />
      </div>
    </main>
  );
}
