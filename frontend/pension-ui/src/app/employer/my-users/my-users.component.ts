import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';


@Component({
  selector: 'app-my-users',
  standalone: true,
  imports: [CommonModule, HttpClientModule, RouterModule],
  templateUrl: './my-users.component.html',
  styleUrls: ['./my-users.component.css']
})
export class MyUsersComponent {
  users: any[] = [];
  errorMsg = '';

  constructor(private http: HttpClient) {
    this.fetchUsers();
  }

  fetchUsers() {
    const token = localStorage.getItem('employerToken');
    const headers = { Authorization: `Bearer ${token}` };

    this.http.get<any>('http://127.0.0.1:5000/api/employer/my-users', { headers }).subscribe({
      next: (res) => {
        this.users = res.users || [];
      },
      error: (err) => {
        this.errorMsg = err.error?.error || 'Failed to load users.';
      }
    });
  }
}
