import LeadFunnel from "@/components/LeadFunnel";

export default function FunnelPage() {
  return (
    <main style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'hsl(var(--nh-slate))' }}>
      {/* Background Decor */}
      <div style={{
        position: 'fixed',
        top: '10%',
        right: '-5%',
        width: '40%',
        height: '60%',
        background: 'hsla(var(--nh-gold), 0.05)',
        filter: 'blur(120px)',
        borderRadius: '100%',
        zIndex: 0
      }} />

      <div style={{ zIndex: 1, width: '100%', paddingTop: '8rem' }}>
        <LeadFunnel />
      </div>
    </main>
  );
}
