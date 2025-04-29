import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {
  profile: any = {};    
  successMsg = '';
  errorMsg = '';

  constructor(private http: HttpClient, private router: Router) {
    this.loadUserProfile();  // ✅ Call to load profile when page loads
  }

  // ✅ 1. Method to load user profile
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
        this.profile = res;  // ✅ Pre-fill form
      },
      error: (err) => {
        console.error('Failed to load profile:', err);
      }
    });
  }

  // ✅ 2. Method to update user profile
  updateProfile() {
    const token = localStorage.getItem('userToken');
    if (!token) {
      this.router.navigate(['/login']);
      return;
    }

    this.http.put<any>('http://127.0.0.1:5000/api/auth/user/update-profile', this.profile, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }).subscribe({
      next: (res) => {
        this.successMsg = res.message;
        this.errorMsg = '';
      },
      error: (err) => {
        this.errorMsg = err.error?.error || 'Profile update failed';
        this.successMsg = '';
      }
    });
  }
}
