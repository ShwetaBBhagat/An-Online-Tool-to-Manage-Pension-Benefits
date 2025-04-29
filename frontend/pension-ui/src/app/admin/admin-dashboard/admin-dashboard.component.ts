import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { Router } from '@angular/router';


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

  constructor(private http: HttpClient, private router: Router) {
    this.loadDashboardStats();
  }

  logoutAdmin() {
    const token = localStorage.getItem('adminToken');
    if (!token) {
      console.error('No admin token found');
      return;
    }
  
    this.http.post<{ message: string }>('http://127.0.0.1:5000/api/admin/logout', {}, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }).subscribe({
      next: (res) => {
        console.log('Admin logged out:', res.message);
        localStorage.removeItem('adminToken');
        this.router.navigate(['/admin/login']);
      },
      error: (err) => {
        console.error('Logout failed:', err);
        localStorage.removeItem('adminToken');
        this.router.navigate(['/admin/login']);
      }
    });
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
