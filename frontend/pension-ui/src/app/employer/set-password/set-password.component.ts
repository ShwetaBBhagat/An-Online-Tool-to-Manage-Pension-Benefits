import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-set-employer-password',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  templateUrl: './set-password.component.html',
  styleUrls: ['./set-password.component.css']
})
export class SetEmployerPasswordComponent {
  password = '';
  confirmPassword = '';
  token = '';
  successMsg = '';
  errorMsg = '';

  constructor(private http: HttpClient, private route: ActivatedRoute, private router: Router) {
    this.token = this.route.snapshot.queryParamMap.get('token') || '';
  }

  submitPassword() {
    if (this.password !== this.confirmPassword) {
      this.errorMsg = "Passwords do not match.";
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
          this.router.navigate(['/employer/login']);
        }, 2000); // Redirect to login after 2 seconds
      },
      error: (err) => {
        this.errorMsg = err.error?.error || 'Failed to set password.';
        this.successMsg = '';
      }
    });
  }
}
