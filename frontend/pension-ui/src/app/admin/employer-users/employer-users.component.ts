import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { isPlatformBrowser } from '@angular/common';
import { inject, PLATFORM_ID } from '@angular/core';

@Component({
  selector: 'app-employer-users',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './employer-users.component.html',
  styleUrls: ['./employer-users.component.css']
})
export class EmployerUsersComponent {
  users: any[] = [];
  employerId = '';
  platformId = inject(PLATFORM_ID);


  constructor(private route: ActivatedRoute, private http: HttpClient) {
    this.route.params.subscribe(params => {
      this.employerId = params['id'];
      console.log('Employer ID:', this.employerId); // ✅ Check if this prints
      this.fetchUsers();
    });
  }

  fetchUsers() {
    if (!isPlatformBrowser(this.platformId)) return;

    const token = localStorage.getItem('adminToken');
    const headers = { Authorization: `Bearer ${token}` };

    this.http.get<any>(`http://127.0.0.1:5000/api/admin/employer/${this.employerId}/users`, { headers }).subscribe({
      next: (res) => {
        this.users = res.users || [];
      },
      error: (err) => {
        console.error('Failed to fetch users:', err);
      }
    });
  }
}
