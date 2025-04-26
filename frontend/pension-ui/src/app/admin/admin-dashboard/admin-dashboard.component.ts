import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, HttpClientModule, RouterModule],
  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['./admin-dashboard.component.css']
})
export class AdminDashboardComponent {
  totalUsers = 0;
  totalEmployers = 0;
  totalDocuments = 0;
  totalStatements = 0;
  totalPotValue = 0;

  constructor(private http: HttpClient) {
    this.loadDashboardStats();
  }

  loadDashboardStats() {
    const token = localStorage.getItem('adminToken');
    const headers = { Authorization: `Bearer ${token}` };

    this.http.get<any>('http://127.0.0.1:5000/api/admin/dashboard-summary', { headers }).subscribe({
      next: (res) => {
        const summary = res.summary;
        this.totalUsers = summary.total_users;
        this.totalEmployers = summary.total_employers;
        this.totalDocuments = summary.total_documents;
        this.totalStatements = summary.total_statements;
        this.totalPotValue = summary.total_pot_value;
      },
      error: (err) => {
        console.error('Error loading dashboard stats:', err);
      }
    });
  }
}
