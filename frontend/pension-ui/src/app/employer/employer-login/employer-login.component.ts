import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-employer-login',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './employer-login.component.html',
  styleUrls: ['./employer-login.component.css']
})
export class EmployerLoginComponent {
  email = '';
  password = '';
  errorMsg = '';

  constructor(private http: HttpClient, private router: Router) {}

  onSubmit() {
    this.http.post<any>('http://127.0.0.1:5000/api/employer/login', {
      email: this.email,
      password: this.password
    }).subscribe({
      next: (res) => {
        localStorage.setItem('employerToken', res.access_token);
        this.router.navigate(['/employer/dashboard']);
      },
      error: (err) => {
        this.errorMsg = err.error?.error || 'Login failed. Please try again.';
      }
    });
  }
}
