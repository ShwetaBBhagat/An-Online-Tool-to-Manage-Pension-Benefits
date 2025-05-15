import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.css']
})
export class EmployerResetPasswordComponent implements OnInit {
  password = '';
  confirmPassword = '';
  token = '';
  errorMsg = '';
  successMsg = '';
  loading = false;

  constructor(private route: ActivatedRoute, private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.token = this.route.snapshot.queryParamMap.get('token') || '';
  }

  submit() {
    if (!this.password || !this.confirmPassword) {
      this.errorMsg = 'Please fill all fields.';
      return;
    }

    if (this.password !== this.confirmPassword) {
      this.errorMsg = 'Passwords do not match.';
      return;
    }

    this.loading = true;
    this.http.post('http://127.0.0.1:5000/api/employer/reset-password', {
      token: this.token,
      password: this.password
    }).subscribe({
      next: res => {
        this.successMsg = 'Password reset successfully. You can now log in.';
        this.errorMsg = '';
        this.loading = false;
      },
      error: err => {
        this.errorMsg = err.error?.error || 'Something went wrong.';
        this.successMsg = '';
        this.loading = false;
      }
    });
  }
}
