'use client';

import React, { useState, useRef, useCallback } from 'react';
import './upload.css';
import { UploadCloud, FileText, X, CheckCircle2, AlertCircle, Loader2, ArrowRight, Shield, Sparkles, Zap, BookOpen } from 'lucide-react';

interface UploadedFile {
  file: File;
  id: string;
  status: 'idle' | 'uploading' | 'success' | 'error';
  progress: number;
  errorMessage?: string;
}

export default function UploadPage() {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const generateId = () => Math.random().toString(36).substring(2, 12);

  const handleFiles = useCallback((selectedFiles: FileList | null) => {
    if (!selectedFiles) return;

    const pdfFiles = Array.from(selectedFiles).filter(
      (f) => f.type === 'application/pdf'
    );

    if (pdfFiles.length === 0) return;

    const newFiles: UploadedFile[] = pdfFiles.map((file) => ({
      file,
      id: generateId(),
      status: 'idle' as const,
      progress: 0,
    }));

    setFiles((prev) => [...prev, ...newFiles]);

    // Simulate upload progress for each file
    newFiles.forEach((uf) => {
      simulateUpload(uf.id);
    });
  }, []);

  const simulateUpload = (fileId: string) => {
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 25 + 10;
      if (progress >= 100) {
        progress = 100;
        clearInterval(interval);
        setFiles((prev) =>
          prev.map((f) =>
            f.id === fileId ? { ...f, status: 'success', progress: 100 } : f
          )
        );
      } else {
        setFiles((prev) =>
          prev.map((f) =>
            f.id === fileId ? { ...f, status: 'uploading', progress } : f
          )
        );
      }
    }, 300);
  };

  const removeFile = (fileId: string) => {
    setFiles((prev) => prev.filter((f) => f.id !== fileId));
  };

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      handleFiles(e.dataTransfer.files);
    },
    [handleFiles]
  );

  const handleAnalyze = async () => {
    if (files.length === 0) return;
    setIsAnalyzing(true);
    // Simulate analysis delay
    setTimeout(() => {
      setIsAnalyzing(false);
      // TODO: integrate with actual API
    }, 3000);
  };

  const allUploaded = files.length > 0 && files.every((f) => f.status === 'success');

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="upload-page">
      {/* Custom Header for Upload Page */}
      <header className="upload-navbar">
        <div className="upload-navbar-inner">
          <a href="/" className="upload-navbar-brand">
            <div className="upload-navbar-logo">RL</div>
            <span className="upload-navbar-name">
              Req<span>Lint</span>
            </span>
            <span className="upload-navbar-tag">Document Analyzer</span>
          </a>
          <nav className="upload-navbar-nav">
            <a href="/" className="upload-nav-link">Text Input</a>
            <a href="/upload" className="upload-nav-link upload-nav-link-active" aria-current="page">Upload PDF</a>
            <a href="/" className="upload-nav-cta">Get Started</a>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-container">
          {/* Left: Headline & Description */}
          <div className="hero-text">
            <div className="hero-badge">
              <Sparkles size={14} />
              <span>AI-Powered Analysis</span>
            </div>
            <h1 className="hero-title">
              <span className="hero-title-line1">Upload Dokumen PDF</span>
              <span className="hero-title-line2">
                untuk <strong>Analisis Requirement.</strong>
              </span>
            </h1>
            <p className="hero-description">
              Unggah dokumen SRS, user story, atau spesifikasi kebutuhan dalam format PDF.
              ReqLint akan menganalisis kualitas requirement berdasarkan kriteria INVEST
              dan format Connextra secara otomatis.
            </p>
            <div className="hero-features">
              <div className="hero-feature">
                <Zap size={18} />
                <span>Analisis Cepat & Akurat</span>
              </div>
              <div className="hero-feature">
                <BookOpen size={18} />
                <span>Mendukung Bahasa ID & EN</span>
              </div>
              <div className="hero-feature">
                <Shield size={18} />
                <span>Dokumen Anda Aman</span>
              </div>
            </div>
          </div>

          {/* Right: Upload Card */}
          <div className="upload-card-wrapper">
            <div className="upload-card">
              {/* Card Tab Bar */}
              <nav className="card-tabs" aria-label="Upload type navigation">
                <a href="/" className="card-tab">
                  <FileText size={18} />
                  <span>Text Input</span>
                </a>
                <a href="/upload" className="card-tab card-tab-active" aria-current="page">
                  <UploadCloud size={18} />
                  <span>Upload PDF</span>
                </a>
              </nav>

              {/* Dropzone */}
              <div className="card-body">
                <div
                  className={`dropzone ${isDragging ? 'dropzone-active' : ''} ${files.length > 0 ? 'dropzone-has-files' : ''}`}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                  role="button"
                  tabIndex={0}
                  aria-label="Upload area, click or drag files here"
                >
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf"
                    multiple
                    onChange={(e) => handleFiles(e.target.files)}
                    className="hidden-input"
                    id="pdf-file-input"
                  />

                  {files.length === 0 ? (
                    <div className="dropzone-empty">
                      <div className="dropzone-icon-wrapper">
                        <UploadCloud size={32} />
                      </div>
                      <p className="dropzone-text-main">
                        Drag & drop file PDF di sini
                      </p>
                      <p className="dropzone-text-sub">
                        atau <span className="dropzone-text-link">klik untuk browse</span>
                      </p>
                      <p className="dropzone-text-hint">
                        Format: PDF • Maks. 10MB per file
                      </p>
                    </div>
                  ) : (
                    <div className="file-list" onClick={(e) => e.stopPropagation()}>
                      {files.map((uf) => (
                        <div key={uf.id} className="file-item">
                          <div className="file-item-icon">
                            <FileText size={20} />
                          </div>
                          <div className="file-item-info">
                            <p className="file-item-name">{uf.file.name}</p>
                            <p className="file-item-size">{formatFileSize(uf.file.size)}</p>
                            {uf.status === 'uploading' && (
                              <div className="progress-bar-track">
                                <div
                                  className="progress-bar-fill"
                                  style={{ width: `${uf.progress}%` }}
                                />
                              </div>
                            )}
                          </div>
                          <div className="file-item-status">
                            {uf.status === 'uploading' && (
                              <Loader2 size={18} className="spin" />
                            )}
                            {uf.status === 'success' && (
                              <CheckCircle2 size={18} className="status-success" />
                            )}
                            {uf.status === 'error' && (
                              <AlertCircle size={18} className="status-error" />
                            )}
                          </div>
                          <button
                            className="file-item-remove"
                            onClick={() => removeFile(uf.id)}
                            aria-label={`Remove ${uf.file.name}`}
                          >
                            <X size={16} />
                          </button>
                        </div>
                      ))}
                      {/* Add more files button */}
                      <button
                        className="add-more-btn"
                        onClick={() => fileInputRef.current?.click()}
                      >
                        <UploadCloud size={16} />
                        <span>Tambah file lain</span>
                      </button>
                    </div>
                  )}
                </div>
              </div>

              {/* Card Footer */}
              <div className="card-footer">
                <div className="card-footer-left">
                  <span className="file-count">
                    {files.length} file{files.length !== 1 ? 's' : ''} dipilih
                  </span>
                </div>
                <div className="card-footer-right">
                  <button
                    className={`analyze-btn ${allUploaded ? 'analyze-btn-ready' : 'analyze-btn-disabled'}`}
                    onClick={handleAnalyze}
                    disabled={!allUploaded || isAnalyzing}
                    id="analyze-button"
                  >
                    {isAnalyzing ? (
                      <>
                        <Loader2 size={18} className="spin" />
                        <span>Menganalisis...</span>
                      </>
                    ) : (
                      <>
                        <span className="analyze-btn-text-lg">Analisis Dokumen</span>
                        <span className="analyze-btn-text-sm">Analisis</span>
                        <ArrowRight size={18} />
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>

            {/* Privacy Guarantee */}
            <div className="privacy-guarantee">
              <Shield size={14} />
              <span>Jaminan Privasi — File Anda tidak disimpan di server</span>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-card-icon feature-icon-blue">
              <FileText size={24} />
            </div>
            <h3 className="feature-card-title">Upload PDF</h3>
            <p className="feature-card-desc">
              Unggah dokumen SRS, BRD, atau user story dalam format PDF untuk dianalisis secara otomatis.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-card-icon feature-icon-emerald">
              <Sparkles size={24} />
            </div>
            <h3 className="feature-card-title">Deteksi Requirement Smell</h3>
            <p className="feature-card-desc">
              AI mengidentifikasi ambiguitas, ketidaklengkapan, dan masalah verifikasi pada setiap requirement.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-card-icon feature-icon-violet">
              <Zap size={24} />
            </div>
            <h3 className="feature-card-title">Skor Kualitas INVEST</h3>
            <p className="feature-card-desc">
              Dapatkan skor kualitas berdasarkan kerangka INVEST dan rekomendasi perbaikan otomatis.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
