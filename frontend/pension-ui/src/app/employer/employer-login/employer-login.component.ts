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
  email: string = '';
  password: string = '';
  mfaToken: string = '';
  showPassword: boolean = false;
  loading: boolean = false;
  errorMsg: string = '';
  requiresMfa: boolean = false;

  constructor(private http: HttpClient, private router: Router) {}

  onSubmit(): void {
    this.errorMsg = '';

    const trimmedEmail = this.email.trim();
    const trimmedPassword = this.password.trim();

    if (!trimmedEmail || !trimmedPassword) {
      this.errorMsg = 'Please enter both email and password.';
      return;
    }

    this.loading = true;

    const payload: any = {
      email: trimmedEmail,
      password: trimmedPassword
    };

    if (this.mfaToken.trim()) {
      payload.mfa_token = this.mfaToken.trim();
    }

    this.http.post<any>('http://127.0.0.1:5000/api/employer/login', payload).subscribe({
      next: (res) => {
        localStorage.setItem('employerToken', res.access_token);
        this.router.navigate(['/employer/dashboard']);
        this.loading = false;
      },
      error: (err) => {
        const backendError = err?.error?.error;
        this.errorMsg = backendError || 'Login failed. Please try again.';
        this.loading = false;

        // If the error mentions MFA, show MFA token field
        if (this.errorMsg.toLowerCase().includes('mfa')) {
          this.requiresMfa = true;
        }
      }
    });
  }
}
