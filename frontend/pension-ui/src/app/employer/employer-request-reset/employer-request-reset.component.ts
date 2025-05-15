import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-employer-request-reset',
  standalone: true,
  templateUrl: './employer-request-reset.component.html',
  styleUrls: ['./employer-request-reset.component.css'],
  imports: [CommonModule, FormsModule, HttpClientModule]
})
export class EmployerRequestResetComponent {
  email: string = '';
  successMsg: string = '';
  errorMsg: string = '';
  loading: boolean = false;

  constructor(private http: HttpClient) {}

  requestReset() {
    this.successMsg = '';
    this.errorMsg = '';
    this.loading = true;

    this.http.post<any>('http://127.0.0.1:5000/api/employer/request-reset', { email: this.email })
      .subscribe({
        next: (res) => {
          this.successMsg = res.message;
          this.loading = false;
        },
        error: (err) => {
          this.errorMsg = err.error?.error || 'Something went wrong.';
          this.loading = false;
        }
      });
  }
}
