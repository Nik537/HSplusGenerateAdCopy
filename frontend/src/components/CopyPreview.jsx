import React from 'react';

const CopyPreview = ({ variants, onExport }) => {
  if (!variants) {
    return (
      <div style={styles.emptyState}>
        <div style={styles.emptyIcon}>📝</div>
        <h3 style={styles.emptyTitle}>No Ad Copy Generated Yet</h3>
        <p style={styles.emptyText}>
          Fill out the form and click "Generate Ad Copy" to create your Facebook ad variants.
        </p>
      </div>
    );
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  const downloadAsText = () => {
    const text = Object.entries(variants)
      .map(([key, variant]) => {
        return `
=== ${key.toUpperCase().replace('_', ' ')} ===
Angle: ${variant.angle}
Hook: ${variant.hook}

Body:
${variant.body}

CTA: ${variant.cta}

Character Count: ${variant.character_count}
${'='.repeat(50)}
`;
      })
      .join('\n');

    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'facebook-ad-copy.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={styles.title}>Generated Ad Copy</h2>
        <button onClick={downloadAsText} style={styles.downloadButton}>
          ⬇️ Download TXT
        </button>
      </div>

      <div style={styles.variantsContainer}>
        {Object.entries(variants).map(([key, variant]) => (
          <AdVariant
            key={key}
            variantName={key}
            variant={variant}
            onCopy={copyToClipboard}
          />
        ))}
      </div>
    </div>
  );
};

const AdVariant = ({ variantName, variant, onCopy }) => {
  const fullCopy = `${variant.hook}\n\n${variant.body}\n\n${variant.cta}`;

  const getScoreColor = (score) => {
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#f59e0b';
    return '#ef4444';
  };

  const getAngleBadgeColor = (angle) => {
    switch(angle) {
      case 'pain_point': return '#dc2626';
      case 'benefit': return '#059669';
      case 'social_proof': return '#2563eb';
      default: return '#6b7280';
    }
  };

  return (
    <div style={styles.variant}>
      <div style={styles.variantHeader}>
        <div style={styles.variantTitle}>
          <span style={styles.variantNumber}>
            {variantName.replace('variant_', 'Variant ')}
          </span>
          <span
            style={{
              ...styles.angleBadge,
              backgroundColor: getAngleBadgeColor(variant.angle)
            }}
          >
            {variant.angle.replace('_', ' ')}
          </span>
        </div>
        <button
          onClick={() => onCopy(fullCopy)}
          style={styles.copyButton}
        >
          📋 Copy
        </button>
      </div>

      <div style={styles.fbPreview}>
        <div style={styles.fbHeader}>
          <div style={styles.fbProfile}>
            <div style={styles.fbAvatar}>HS</div>
            <div>
              <div style={styles.fbPageName}>HS Plus</div>
              <div style={styles.fbSponsored}>Sponsored</div>
            </div>
          </div>
        </div>

        <div style={styles.fbContent}>
          <div style={styles.hookText}>{variant.hook}</div>
          <div style={styles.bodyText}>{variant.body}</div>
          <div style={styles.ctaText}>{variant.cta}</div>
        </div>
      </div>

      <div style={styles.stats}>
        <div style={styles.stat}>
          <span style={styles.statLabel}>Characters:</span>
          <span style={styles.statValue}>{variant.character_count}</span>
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '24px',
    height: '100%',
    overflowY: 'auto',
    backgroundColor: '#fff'
  },
  emptyState: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100%',
    padding: '48px',
    textAlign: 'center'
  },
  emptyIcon: {
    fontSize: '64px',
    marginBottom: '16px',
    opacity: 0.5
  },
  emptyTitle: {
    fontSize: '20px',
    fontWeight: '600',
    color: '#333',
    marginBottom: '8px'
  },
  emptyText: {
    fontSize: '14px',
    color: '#666',
    lineHeight: '1.5',
    maxWidth: '400px'
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '24px'
  },
  title: {
    fontSize: '24px',
    fontWeight: '700',
    color: '#1a1a1a'
  },
  downloadButton: {
    padding: '10px 16px',
    fontSize: '14px',
    fontWeight: '500',
    color: '#fff',
    backgroundColor: '#10b981',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'background-color 0.2s'
  },
  variantsContainer: {
    display: 'flex',
    flexDirection: 'column',
    gap: '24px'
  },
  variant: {
    border: '1px solid #e5e7eb',
    borderRadius: '12px',
    padding: '20px',
    backgroundColor: '#fafafa'
  },
  variantHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '16px'
  },
  variantTitle: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px'
  },
  variantNumber: {
    fontSize: '16px',
    fontWeight: '700',
    color: '#1a1a1a'
  },
  angleBadge: {
    padding: '4px 12px',
    fontSize: '12px',
    fontWeight: '600',
    color: 'white',
    borderRadius: '12px',
    textTransform: 'capitalize'
  },
  copyButton: {
    padding: '8px 16px',
    fontSize: '13px',
    fontWeight: '500',
    color: '#1877f2',
    backgroundColor: 'white',
    border: '1px solid #1877f2',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'all 0.2s'
  },
  fbPreview: {
    backgroundColor: 'white',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    overflow: 'hidden',
    marginBottom: '16px'
  },
  fbHeader: {
    padding: '12px',
    borderBottom: '1px solid #e5e7eb'
  },
  fbProfile: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px'
  },
  fbAvatar: {
    width: '40px',
    height: '40px',
    borderRadius: '50%',
    backgroundColor: '#1877f2',
    color: 'white',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: '700',
    fontSize: '14px'
  },
  fbPageName: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#1a1a1a'
  },
  fbSponsored: {
    fontSize: '12px',
    color: '#65676b'
  },
  fbContent: {
    padding: '12px'
  },
  hookText: {
    fontSize: '15px',
    fontWeight: '700',
    color: '#1a1a1a',
    marginBottom: '8px',
    lineHeight: '1.4'
  },
  bodyText: {
    fontSize: '14px',
    color: '#1a1a1a',
    lineHeight: '1.5',
    marginBottom: '12px',
    whiteSpace: 'pre-wrap'
  },
  ctaText: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#1877f2'
  },
  stats: {
    display: 'flex',
    gap: '24px',
    paddingTop: '12px',
    borderTop: '1px solid #e5e7eb'
  },
  stat: {
    display: 'flex',
    gap: '8px',
    fontSize: '13px'
  },
  statLabel: {
    color: '#666',
    fontWeight: '500'
  },
  statValue: {
    color: '#1a1a1a',
    fontWeight: '700'
  }
};

export default CopyPreview;
