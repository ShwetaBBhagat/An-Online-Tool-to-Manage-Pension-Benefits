import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';


@Component({
  selector: 'app-all-users',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule, RouterModule],
  templateUrl: './all-users.component.html',
  styleUrls: ['./all-users.component.css']
})
export class AllUsersComponent {
  users: any[] = [];
  platformId = inject(PLATFORM_ID);


  // Filters
  email: string = '';
  profileCompleted: string = '';

  constructor(private http: HttpClient) {
    this.fetchUsers();
  }

  fetchUsers() {
    if (!isPlatformBrowser(this.platformId)) {
      return; // Skip on server-side
    }
    const token = localStorage.getItem('adminToken');
    const headers = { Authorization: `Bearer ${token}` };

    const params: any = {};
    if (this.email) params.email = this.email;
    if (this.profileCompleted) params.profile_completed = this.profileCompleted;

    this.http.get<any>('http://127.0.0.1:5000/api/admin/users', { headers, params }).subscribe({
      next: (res) => {
        this.users = res.users || [];
      },
      error: (err) => {
        console.error('Error fetching users:', err);
      }
    });
  }

  onResetFilters() {
    this.email = '';
    this.profileCompleted = '';
    this.fetchUsers();
  }
}
