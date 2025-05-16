import { Component, ChangeDetectorRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import Chart from 'chart.js/auto';

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.css']
})
export class AnalyticsComponent {
  analytics: any = null;
  contributionsChart: any = null;
  isLoading = true;

  constructor(private http: HttpClient, private cdr: ChangeDetectorRef) {
    this.loadAnalytics();
  }

  loadAnalytics() {
    this.isLoading = true;

    const token = localStorage.getItem('userToken');

    this.http.get<any>('http://127.0.0.1:5000/api/auth/user/analytics', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }).subscribe({
      next: (res) => {
        if (res.status === 'success') {
          this.analytics = res.analytics;

          // Wait for Angular to detect new DOM, then initialize chart
          this.cdr.detectChanges(); // Force detect changes manually
          setTimeout(() => {
            this.initializeChart();
          }, 0);
        }
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Error fetching analytics:', err);
        this.isLoading = false;
      }
    });
  }

  initializeChart() {
    if (!this.analytics?.contributions_chart?.length) {
      console.error('No contributions_chart data');
      return;
    }

    const canvas = document.getElementById('contributionsChart') as HTMLCanvasElement;
    if (!canvas) {
      console.error('Canvas element not found');
      return;
    }

    const ctx = canvas.getContext('2d');
    if (!ctx) {
      console.error('Canvas 2D context not available');
      return;
    }

    if (this.contributionsChart) {
      this.contributionsChart.destroy();
    }

    this.contributionsChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: this.analytics.contributions_chart.map((c: any) => c.month),
        datasets: [
          {
            label: 'Employee Contribution (£)',
            data: this.analytics.contributions_chart.map((c: any) => c.employee_contribution),
            borderColor: 'blue',
            backgroundColor: 'blue',
            fill: false,
            tension: 0.4
          },
          {
            label: 'Employer Contribution (£)',
            data: this.analytics.contributions_chart.map((c: any) => c.employer_contribution),
            borderColor: 'green',
            backgroundColor: 'green',
            fill: false,
            tension: 0.4
          },
          {
            label: 'Pot Value (£)',
            data: this.analytics.contributions_chart.map((c: any) => c.pot_value),
            borderColor: 'purple',
            backgroundColor: 'purple',
            fill: false,
            tension: 0.4
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom'
          },
          tooltip: {
            enabled: true
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  }
}
