import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';      
import { CommonModule } from '@angular/common';     
import { ActivatedRoute } from '@angular/router';   

@Component({
  selector: 'app-reset-password',
  standalone: true,           // ✅ Standalone component
  imports: [FormsModule, CommonModule],
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.css']
})
export class ResetPasswordComponent {
  token = '';
  newPassword = '';
  successMsg = '';
  errorMsg = '';

  constructor(private http: HttpClient, private route: ActivatedRoute) {
    this.route.queryParams.subscribe(params => {
      this.token = params['token'] || '';
    });
  }

  resetPassword() {
    const payload = {
      token: this.token,
      password: this.newPassword
    };

    this.http.post<any>('http://127.0.0.1:5000/api/auth/reset-password', payload)
      .subscribe({
        next: (response) => {
          this.successMsg = response.message;
          this.errorMsg = '';
        },
        error: (error) => {
          this.errorMsg = error.error.error || 'Reset failed';
          this.successMsg = '';
        }
      });
  }
}
