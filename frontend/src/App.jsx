import React, { useState, useEffect } from 'react';
import InputForm from './components/InputForm';
import CopyPreview from './components/CopyPreview';
import { api } from './utils/api';

function App() {
  const [formData, setFormData] = useState({
    url: '',
    product_name: '',
    price: '',
    features: '',
    market: 'SI',
    objective: 'Conversion',
    description: '',
    model: 'fast'  // Default to fast (Haiku 4.5)
  });

  const [variants, setVariants] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [examples, setExamples] = useState([]);
  const [apiStatus, setApiStatus] = useState({ healthy: false, claude_configured: false });

  useEffect(() => {
    // Load examples on mount
    loadExamples();
    checkApiHealth();
  }, []);

  useEffect(() => {
    // Auto-scrape when URL changes
    if (formData.url && formData.url.includes('vigoshop.si')) {
      handleScrape();
    }
  }, [formData.url]);

  const checkApiHealth = async () => {
    try {
      const response = await api.healthCheck();
      setApiStatus({
        healthy: response.status === 'healthy',
        claude_configured: response.claude_api_configured
      });
    } catch (err) {
      console.error('API health check failed:', err);
    }
  };

  const loadExamples = async () => {
    try {
      const response = await api.getExamples();
      if (response.success) {
        setExamples(response.examples);
      }
    } catch (err) {
      console.error('Failed to load examples:', err);
    }
  };

  const handleScrape = async () => {
    if (!formData.url) return;

    try {
      setLoading(true);
      setError(null);

      const response = await api.scrapeProduct(formData.url);

      if (response.success) {
        setFormData(prev => ({
          ...prev,
          product_name: response.data.name || prev.product_name,
          price: response.data.price || prev.price,
          features: response.data.features || prev.features,
          description: response.data.description || prev.description
        }));
      } else {
        setError(response.error || 'Failed to scrape product');
      }
    } catch (err) {
      console.error('Scraping error:', err);
      setError('Failed to scrape product. Please fill in details manually.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await api.generateCopy({
        product_name: formData.product_name,
        price: formData.price,
        features: formData.features,
        market: formData.market,
        objective: formData.objective,
        description: formData.description,
        model: formData.model
      });

      if (response.success) {
        setVariants(response.data);
      } else {
        setError(response.error || 'Failed to generate copy');
      }
    } catch (err) {
      console.error('Generation error:', err);
      setError(err.response?.data?.error || 'Failed to generate copy. Please check your API configuration.');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadExample = (index) => {
    if (examples[index]) {
      const example = examples[index];
      setFormData({
        url: example.url,
        product_name: example.product_name,
        price: example.price,
        features: example.features,
        market: example.market,
        objective: example.objective,
        description: ''
      });
      setVariants(null); // Clear previous results
    }
  };

  return (
    <div style={styles.app}>
      {/* Header */}
      <header style={styles.header}>
        <div style={styles.headerContent}>
          <h1 style={styles.logo}>⚡ Marketing Copy Generator</h1>
          <div style={styles.statusIndicator}>
            {apiStatus.healthy ? (
              <span style={styles.statusHealthy}>
                ✅ API Connected
                {!apiStatus.claude_configured && ' (Claude API not configured)'}
              </span>
            ) : (
              <span style={styles.statusError}>❌ API Disconnected</span>
            )}
          </div>
        </div>
      </header>

      {/* Error Banner */}
      {error && (
        <div style={styles.errorBanner}>
          <span>⚠️ {error}</span>
          <button onClick={() => setError(null)} style={styles.closeError}>
            ✕
          </button>
        </div>
      )}

      {/* Main Content */}
      <div style={styles.main}>
        {/* Left Panel - Input Form */}
        <div style={styles.leftPanel}>
          <InputForm
            formData={formData}
            setFormData={setFormData}
            onSubmit={handleSubmit}
            loading={loading}
            onLoadExample={handleLoadExample}
          />
        </div>

        {/* Right Panel - Preview */}
        <div style={styles.rightPanel}>
          <CopyPreview variants={variants} />
        </div>
      </div>
    </div>
  );
}

const styles = {
  app: {
    height: '100vh',
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: '#f5f5f5'
  },
  header: {
    backgroundColor: '#1877f2',
    color: 'white',
    padding: '16px 24px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
  },
  headerContent: {
    maxWidth: '1600px',
    margin: '0 auto',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  },
  logo: {
    fontSize: '20px',
    fontWeight: '700',
    margin: 0
  },
  statusIndicator: {
    fontSize: '13px'
  },
  statusHealthy: {
    color: '#d1fae5',
    fontWeight: '500'
  },
  statusError: {
    color: '#fecaca',
    fontWeight: '500'
  },
  errorBanner: {
    backgroundColor: '#fee2e2',
    color: '#991b1b',
    padding: '12px 24px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    fontSize: '14px',
    fontWeight: '500'
  },
  closeError: {
    background: 'none',
    border: 'none',
    color: '#991b1b',
    fontSize: '18px',
    cursor: 'pointer',
    padding: '0 8px'
  },
  main: {
    flex: 1,
    display: 'flex',
    maxWidth: '1600px',
    margin: '0 auto',
    width: '100%',
    overflow: 'hidden'
  },
  leftPanel: {
    width: '40%',
    minWidth: '400px',
    backgroundColor: 'white',
    borderRight: '1px solid #e5e7eb',
    overflowY: 'auto'
  },
  rightPanel: {
    flex: 1,
    backgroundColor: '#fff',
    overflowY: 'auto'
  }
};

export default App;
