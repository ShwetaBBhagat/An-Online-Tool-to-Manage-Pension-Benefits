import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-admin-login',
  imports: [CommonModule, FormsModule, RouterModule, HttpClientModule ],
  templateUrl: './admin-login.component.html',
  styleUrls: ['./admin-login.component.css']
})

export class AdminLoginComponent {
  admin = {
    email: '',
    password: '',
  };

  errorMessage = '';
  showPassword = false;


  constructor(private http: HttpClient, private router: Router) {}

  onSubmit() {
    this.http.post<any>('http://127.0.0.1:5000/api/admin/login', this.admin).subscribe({
      next: (res: any) => {
        localStorage.setItem('adminToken', res.access_token); // Store JWT token
        alert('Login successful!');
        this.router.navigate(['/admin/dashboard']);
      },
      error: (err: any) => {
        this.errorMessage = err.error?.error || 'Login failed. Please try again.';
      }
    });
  }  
}
