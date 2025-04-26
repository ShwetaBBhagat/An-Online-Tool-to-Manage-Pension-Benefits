import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-employer-dashboard',
  standalone: true,
  imports: [CommonModule, HttpClientModule, RouterModule],
  templateUrl: './employer-dashboard.component.html',
  styleUrls: ['./employer-dashboard.component.css']
})
export class EmployerDashboardComponent {
  summary: any = null;
  errorMsg = '';

  constructor(private http: HttpClient) {
    this.fetchSummary();
  }

  fetchSummary() {
    const token = localStorage.getItem('employerToken');
    const headers = { Authorization: `Bearer ${token}` };

    this.http.get<any>('http://127.0.0.1:5000/api/employer/dashboard-summary', { headers }).subscribe({
      next: (res) => {
        this.summary = res.summary;
      },
      error: (err) => {
        this.errorMsg = err.error?.error || 'Failed to load dashboard summary.';
      }
    });
  }
}
