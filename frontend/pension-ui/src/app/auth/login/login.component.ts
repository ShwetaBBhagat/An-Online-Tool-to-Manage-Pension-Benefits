import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email = '';
  password = '';
  mfaToken = '';
  successMsg = '';
  errorMsg = '';
  showPassword: boolean = false;

  constructor(private http: HttpClient, private router: Router) {}

  login() {
    this.http.post<any>('http://127.0.0.1:5000/api/auth/login', {
      email: this.email,
      password: this.password,
      mfa_token: this.mfaToken
    }).subscribe({
      next: (res) => {
        localStorage.setItem('userToken', res.access_token);
        this.successMsg = res.message;
        this.errorMsg = '';

        // Redirect based on role
        if (res.role === 'user') {
          this.router.navigate(['/dashboard']);
        } 
      },
      error: (err) => {
        this.errorMsg = err.error?.error || 'Login failed.';
        this.successMsg = '';
      }
    });
  }
}
