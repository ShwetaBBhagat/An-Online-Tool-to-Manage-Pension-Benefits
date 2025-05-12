import { Component, AfterViewInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
declare var bootstrap: any;

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements AfterViewInit {
  user: any = {};
  modalShown = false;

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
        this.user = res;
        // Show modal if profile is incomplete and modal hasn't been shown yet
        setTimeout(() => this.checkAndShowReminder(), 500);
      },
      error: (err) => {
        console.error('Failed to load user profile:', err);
      }
    });
  }

  ngAfterViewInit(): void {
    // Optional safety call — modal will only show after user is loaded
  }

  checkAndShowReminder(): void {
    if (this.isProfileIncomplete() && !this.modalShown) {
      const modal = new bootstrap.Modal(document.getElementById('incompleteProfileModal'));
      modal.show();
      this.modalShown = true;
    }
  }

  isProfileIncomplete(): boolean {
    const requiredFields = [
      'email', 'ni_number', 'date_of_birth', 'current_salary',
      'employment_status', 'investment_type', 'postal_code', 'contact_number'
    ];
    return requiredFields.some(field => !this.user?.[field]);
  }

  logout() {
    const token = localStorage.getItem('userToken');

    if (!token) {
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
        localStorage.removeItem('userToken');
        this.router.navigate(['/login']);
      },
      error: (error) => {
        console.error('Logout error:', error);
        localStorage.removeItem('userToken');
        this.router.navigate(['/login']);
      }
    });
  }
}
