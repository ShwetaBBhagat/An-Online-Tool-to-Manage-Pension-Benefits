import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { inject, PLATFORM_ID } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-employer-users',
  standalone: true,
  imports: [CommonModule, HttpClientModule, RouterModule],
  templateUrl: './employer-users.component.html',
  styleUrls: ['./employer-users.component.css']
})
export class EmployerUsersComponent {
  users: any[] = [];
  employerId: string = '';
  loading: boolean = false;
  platformId = inject(PLATFORM_ID);

  constructor(private route: ActivatedRoute, private http: HttpClient) {
    this.route.params.subscribe(params => {
      this.employerId = params['id'];
      console.log('Employer ID:', this.employerId); // For debugging
      this.fetchUsers();
    });
  }

  fetchUsers() {
    if (!isPlatformBrowser(this.platformId)) return;

    const token = localStorage.getItem('adminToken');
    if (!token) {
      console.error('No admin token found.');
      return;
    }

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });

    this.loading = true; // Start loading
    this.http.get<any>(`http://127.0.0.1:5000/api/admin/employer/${this.employerId}/users`, { headers }).subscribe({
      next: (res) => {
        this.users = res.users || [];
        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to fetch users:', err);
        this.loading = false;
      }
    });
  }
}
