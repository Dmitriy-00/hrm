/**
 * Radar chart for multi-dimensional score visualization
 */
'use client';

import { useEffect, useRef } from 'react';

interface DataPoint {
  label: string;
  value: number;
}

interface RadarChartProps {
  data: DataPoint[];
  size?: number;
  className?: string;
}

export function RadarChart({ data, size = 300, className = '' }: RadarChartProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, size, size);

    const centerX = size / 2;
    const centerY = size / 2;
    const radius = size / 2 - 60;
    const levels = 5;
    const angleStep = (Math.PI * 2) / data.length;

    // Draw background levels
    ctx.strokeStyle = '#e5e7eb';
    ctx.lineWidth = 1;
    for (let level = 1; level <= levels; level++) {
      const levelRadius = (radius / levels) * level;
      ctx.beginPath();
      for (let i = 0; i <= data.length; i++) {
        const angle = i * angleStep - Math.PI / 2;
        const x = centerX + levelRadius * Math.cos(angle);
        const y = centerY + levelRadius * Math.sin(angle);
        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }
      ctx.closePath();
      ctx.stroke();
    }

    // Draw axes
    ctx.strokeStyle = '#d1d5db';
    ctx.lineWidth = 1;
    for (let i = 0; i < data.length; i++) {
      const angle = i * angleStep - Math.PI / 2;
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(x, y);
      ctx.stroke();
    }

    // Draw data polygon
    ctx.fillStyle = 'rgba(59, 130, 246, 0.2)';
    ctx.strokeStyle = '#3b82f6';
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (let i = 0; i <= data.length; i++) {
      const point = data[i % data.length];
      const angle = i * angleStep - Math.PI / 2;
      const value = point.value / 100;
      const distance = radius * value;
      const x = centerX + distance * Math.cos(angle);
      const y = centerY + distance * Math.sin(angle);
      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    }
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    // Draw points
    ctx.fillStyle = '#3b82f6';
    for (let i = 0; i < data.length; i++) {
      const point = data[i];
      const angle = i * angleStep - Math.PI / 2;
      const value = point.value / 100;
      const distance = radius * value;
      const x = centerX + distance * Math.cos(angle);
      const y = centerY + distance * Math.sin(angle);
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fill();
    }

    // Draw labels
    ctx.fillStyle = '#374151';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    for (let i = 0; i < data.length; i++) {
      const point = data[i];
      const angle = i * angleStep - Math.PI / 2;
      const labelDistance = radius + 30;
      const x = centerX + labelDistance * Math.cos(angle);
      const y = centerY + labelDistance * Math.sin(angle);

      // Draw label background
      const metrics = ctx.measureText(point.label);
      const labelWidth = metrics.width + 8;
      const labelHeight = 20;
      ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
      ctx.fillRect(x - labelWidth / 2, y - labelHeight / 2, labelWidth, labelHeight);

      // Draw label text
      ctx.fillStyle = '#374151';
      ctx.fillText(point.label, x, y);

      // Draw value
      ctx.fillStyle = '#6b7280';
      ctx.font = 'bold 10px sans-serif';
      ctx.fillText(`${Math.round(point.value)}%`, x, y + 12);
      ctx.font = '12px sans-serif';
    }
  }, [data, size]);

  return (
    <div className={className}>
      <canvas
        ref={canvasRef}
        width={size}
        height={size}
        className="mx-auto"
      />
    </div>
  );
}
