import LeadFunnel from "@/components/LeadFunnel";

export default function FunnelPage() {
  return (
    <main style={{ minHeight: '100vh', background: 'hsl(var(--background))' }}>
      <div className="nh-blue-box gliding-box" style={{ 
        margin: '0 auto', 
        minHeight: '100vh', 
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative'
      }}>
        {/* Background Decor */}
        <div style={{
          position: 'absolute',
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
      </div>
    </main>
  );
}
