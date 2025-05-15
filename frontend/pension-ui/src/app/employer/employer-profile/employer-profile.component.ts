import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-employer-profile',
  standalone: true,
  imports: [CommonModule, HttpClientModule,FormsModule, RouterModule],
  templateUrl: './employer-profile.component.html',
  styleUrls: ['./employer-profile.component.css']
})
export class EmployerProfileComponent {
  profile: any = null;
  errorMsg = '';
  successMsg = '';

  editContactNumber = '';
  editAddress = '';

  constructor(private http: HttpClient) {
    this.fetchProfile();
  }

  fetchProfile() {
    const token = localStorage.getItem('employerToken');
    const headers = { Authorization: `Bearer ${token}` };

    this.http.get<any>('http://127.0.0.1:5000/api/employer/profile', { headers }).subscribe({
      next: (res) => {
        this.profile = res.profile;
        this.editContactNumber = this.profile.contact_number;
        this.editAddress = this.profile.address;
      },
      error: (err) => {
        this.errorMsg = err.error?.error || 'Failed to load profile.';
      }
    });
  }

  updateProfile() {
    const token = localStorage.getItem('employerToken');
    const headers = { Authorization: `Bearer ${token}` };

    this.http.put<any>('http://127.0.0.1:5000/api/employer/update-profile', {
      contact_number: this.editContactNumber,
      address: this.editAddress
    }, { headers }).subscribe({
      next: (res) => {
        this.successMsg = res.message;
        this.errorMsg = '';
        this.fetchProfile(); // Refresh profile
      },
      error: (err) => {
        this.errorMsg = err.error?.error || 'Failed to update profile.';
        this.successMsg = '';
      }
    });
  }
}
