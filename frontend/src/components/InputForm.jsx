import React from 'react';

const InputForm = ({ formData, setFormData, onSubmit, loading, onLoadExample }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSelectChange = (e, fieldName, customFieldName) => {
    const { value } = e.target;
    if (value === 'custom') {
      setFormData(prev => ({ ...prev, [customFieldName]: true, [fieldName]: '' }));
    } else {
      setFormData(prev => ({ ...prev, [customFieldName]: false, [fieldName]: value }));
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Facebook Ad Copy Generator</h2>

      <form onSubmit={onSubmit} style={styles.form}>
        <div style={styles.formGroup}>
          <label style={styles.label}>Product URL (vigoshop.si)</label>
          <input
            type="url"
            name="url"
            value={formData.url}
            onChange={handleChange}
            placeholder="https://vigoshop.si/izdelek/product-name/"
            style={styles.input}
          />
          <small style={styles.hint}>Paste URL to auto-fill product details</small>
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Product Name *</label>
          <input
            type="text"
            name="product_name"
            value={formData.product_name}
            onChange={handleChange}
            placeholder="e.g., Električni čistilec zob SMILY"
            style={styles.input}
            required
          />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Price *</label>
          <input
            type="text"
            name="price"
            value={formData.price}
            onChange={handleChange}
            placeholder="e.g., 19,99€"
            style={styles.input}
            required
          />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Key Features *</label>
          <textarea
            name="features"
            value={formData.features}
            onChange={handleChange}
            placeholder="Feature 1 | Feature 2 | Feature 3&#10;e.g., Removes plaque | USB rechargeable | 3 modes"
            style={{ ...styles.input, ...styles.textarea }}
            rows="4"
            required
          />
        </div>

        <div style={styles.formRow}>
          <div style={{ ...styles.formGroup, flex: 1 }}>
            <label style={styles.label}>Target Market *</label>
            {!formData.customMarket ? (
              <select
                name="market"
                value={formData.market}
                onChange={(e) => handleSelectChange(e, 'market', 'customMarket')}
                style={styles.select}
                required
              >
                <option value="Slovenia">Slovenia (SI)</option>
                <option value="Germany">Germany (DE)</option>
                <option value="Italy">Italy (IT)</option>
                <option value="Austria">Austria (AT)</option>
                <option value="Croatia">Croatia (HR)</option>
                <option value="Bosnia">Bosnia (BA)</option>
                <option value="custom">✏️ Custom</option>
              </select>
            ) : (
              <div style={{ display: 'flex', gap: '8px' }}>
                <input
                  type="text"
                  name="market"
                  value={formData.market}
                  onChange={handleChange}
                  placeholder="Enter custom market"
                  style={{ ...styles.input, flex: 1 }}
                  required
                />
                <button
                  type="button"
                  onClick={() => setFormData(prev => ({ ...prev, customMarket: false, market: 'Slovenia' }))}
                  style={styles.resetButton}
                >
                  ↶
                </button>
              </div>
            )}
          </div>

          <div style={{ ...styles.formGroup, flex: 1 }}>
            <label style={styles.label}>Ad Objective *</label>
            {!formData.customObjective ? (
              <select
                name="objective"
                value={formData.objective}
                onChange={(e) => handleSelectChange(e, 'objective', 'customObjective')}
                style={styles.select}
                required
              >
                <option value="Awareness">Awareness</option>
                <option value="Conversion">Conversion</option>
                <option value="Engagement">Engagement</option>
                <option value="custom">✏️ Custom</option>
              </select>
            ) : (
              <div style={{ display: 'flex', gap: '8px' }}>
                <input
                  type="text"
                  name="objective"
                  value={formData.objective}
                  onChange={handleChange}
                  placeholder="Enter custom objective"
                  style={{ ...styles.input, flex: 1 }}
                  required
                />
                <button
                  type="button"
                  onClick={() => setFormData(prev => ({ ...prev, customObjective: false, objective: 'Conversion' }))}
                  style={styles.resetButton}
                >
                  ↶
                </button>
              </div>
            )}
          </div>
        </div>

        <div style={styles.formRow}>
          <div style={{ ...styles.formGroup, flex: '0 0 35%' }}>
            <label style={styles.label}>AI Model</label>
            <select
              name="model"
              value={formData.model}
              onChange={handleChange}
              style={styles.select}
            >
              <option value="fast">⚡ Fast (Haiku)</option>
              <option value="smart">🧠 Smart (Sonnet)</option>
            </select>
            <small style={styles.hint}>Fast: 2-3s | Smart: 5-8s</small>
          </div>

          <div style={{ ...styles.formGroup, flex: '1' }}>
            <label style={styles.label}>Max Characters</label>
            {!formData.customMaxChars ? (
              <select
                name="max_chars"
                value={formData.max_chars}
                onChange={(e) => handleSelectChange(e, 'max_chars', 'customMaxChars')}
                style={styles.select}
              >
                <option value="125">125 characters (Mobile)</option>
                <option value="150">150 characters (Recommended)</option>
                <option value="200">200 characters (Extended)</option>
                <option value="300">300 characters (Long form)</option>
                <option value="custom">✏️ Custom</option>
              </select>
            ) : (
              <div style={{ display: 'flex', gap: '8px' }}>
                <input
                  type="number"
                  name="max_chars"
                  value={formData.max_chars}
                  onChange={handleChange}
                  placeholder="Enter custom limit"
                  min="50"
                  max="650"
                  style={{ ...styles.input, flex: 1 }}
                  required
                />
                <button
                  type="button"
                  onClick={() => setFormData(prev => ({ ...prev, customMaxChars: false, max_chars: '150' }))}
                  style={styles.resetButton}
                >
                  ↶
                </button>
              </div>
            )}
            <small style={styles.hint}>Shorter copy performs better on mobile</small>
          </div>
        </div>

        <button
          type="submit"
          style={{
            ...styles.button,
            ...(loading ? styles.buttonDisabled : {})
          }}
          disabled={loading}
        >
          {loading ? 'Generating...' : '✨ Generate Ad Copy'}
        </button>
      </form>
    </div>
  );
};

const styles = {
  container: {
    padding: '24px',
    height: '100%',
    overflowY: 'auto'
  },
  title: {
    fontSize: '24px',
    fontWeight: '700',
    marginBottom: '24px',
    color: '#1a1a1a'
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px'
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '6px'
  },
  formRow: {
    display: 'flex',
    gap: '16px'
  },
  label: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#333'
  },
  input: {
    padding: '10px 12px',
    fontSize: '14px',
    border: '1px solid #ddd',
    borderRadius: '6px',
    outline: 'none',
    transition: 'border-color 0.2s',
    fontFamily: 'inherit'
  },
  textarea: {
    resize: 'vertical',
    minHeight: '80px',
    lineHeight: '1.5'
  },
  select: {
    padding: '10px 12px',
    fontSize: '14px',
    border: '1px solid #ddd',
    borderRadius: '6px',
    outline: 'none',
    backgroundColor: 'white',
    cursor: 'pointer'
  },
  hint: {
    fontSize: '12px',
    color: '#666',
    fontStyle: 'italic'
  },
  button: {
    padding: '14px 24px',
    fontSize: '16px',
    fontWeight: '600',
    color: 'white',
    backgroundColor: '#1877f2',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
    marginTop: '8px'
  },
  buttonDisabled: {
    backgroundColor: '#ccc',
    cursor: 'not-allowed'
  },
  examplesSection: {
    marginTop: '16px',
    paddingTop: '20px',
    borderTop: '1px solid #eee',
    display: 'flex',
    flexDirection: 'column',
    gap: '12px'
  },
  examplesLabel: {
    fontSize: '13px',
    color: '#666',
    fontWeight: '500'
  },
  exampleButton: {
    padding: '10px 16px',
    fontSize: '14px',
    fontWeight: '500',
    color: '#1877f2',
    backgroundColor: 'white',
    border: '1px solid #1877f2',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'all 0.2s'
  },
  resetButton: {
    padding: '10px 14px',
    fontSize: '16px',
    fontWeight: '500',
    color: '#666',
    backgroundColor: '#f3f4f6',
    border: '1px solid #ddd',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'all 0.2s',
    minWidth: '44px'
  }
};

export default InputForm;
