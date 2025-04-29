import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-set-password',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './set-password.component.html',
  styleUrls: ['./set-password.component.css']
})
export class SetPasswordComponent implements OnInit {
  password = '';
  confirmPassword = '';
  token = '';
  errorMsg = '';
  successMsg = '';
  passwordStrength = '';

  constructor(private http: HttpClient, private route: ActivatedRoute, private router: Router) {}

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.token = params['token'];
    });
  }

  submitPassword() {
    if (this.password !== this.confirmPassword) {
      this.errorMsg = "Passwords do not match!";
      this.successMsg = '';
      return;
    }

    this.http.post<any>('http://127.0.0.1:5000/api/employer/set-password', {
      token: this.token,
      password: this.password
    }).subscribe({
      next: (res) => {
        this.successMsg = res.message;
        this.errorMsg = '';
        setTimeout(() => {
          this.router.navigate(['/employer-login']);
        }, 1500);
      },
      error: (err) => {
        this.errorMsg = err.error?.error || 'Something went wrong.';
        this.successMsg = '';
      }
    });
  }

  checkPasswordStrength() {
    const strongPassword = new RegExp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$');
    const mediumPassword = new RegExp('^(?=.*[a-z])(?=.*\\d)[A-Za-z\\d]{6,}$');

    if (strongPassword.test(this.password)) {
      this.passwordStrength = 'Strong';
    } else if (mediumPassword.test(this.password)) {
      this.passwordStrength = 'Medium';
    } else {
      this.passwordStrength = 'Weak';
    }
  }
}
