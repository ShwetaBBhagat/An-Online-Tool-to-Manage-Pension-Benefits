import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  user: any = {};
  constructor(private http: HttpClient, private router: Router) {
    this.loadUserProfile();
  }

  loadUserProfile() {
    const token = localStorage.getItem('userToken');
    if (!token) {
      this.router.navigate(['/login']);
      return;
    }

    this.http.get<any>('http://127.0.0.1:5000/api/auth/user/profile', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }).subscribe({
      next: (res) => {
        this.user = res;  // ✅ Save user data
      },
      error: (err) => {
        console.error('Failed to load user profile:', err);
      }
    });
  }

  logout() {
    const token = localStorage.getItem('userToken');

    if (!token) {
      // No token available, just redirect to login
      this.router.navigate(['/login']);
      return;
    }

    this.http.post<any>('http://127.0.0.1:5000/api/auth/logout', {}, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }).subscribe({
      next: (response) => {
        console.log(response.message);
        localStorage.removeItem('userToken');  // Remove token from local storage
        this.router.navigate(['/login']);      // Redirect to login page
      },
      error: (error) => {
        console.error('Logout error:', error);
        // Still remove token and redirect even if error
        localStorage.removeItem('userToken');
        this.router.navigate(['/login']);
      }
    });
  }
}
