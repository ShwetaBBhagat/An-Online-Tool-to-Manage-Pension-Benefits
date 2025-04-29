import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';      // ✅ Important for ngModel
import { CommonModule } from '@angular/common';     // ✅ Important for *ngIf

@Component({
  selector: 'app-request-reset',
  standalone: true,           // ✅ Standalone component
  imports: [FormsModule, CommonModule], // ✅ Declare required modules
  templateUrl: './request-reset.component.html',
  styleUrls: ['./request-reset.component.css']
})
export class RequestResetComponent {
  email = '';
  successMsg = '';
  errorMsg = '';

  constructor(private http: HttpClient) {}

  requestReset() {
    const payload = { email: this.email };

    this.http.post<any>('http://127.0.0.1:5000/api/auth/request-reset', payload)
      .subscribe({
        next: (response) => {
          this.successMsg = response.message;
          this.errorMsg = '';
        },
        error: (error) => {
          this.errorMsg = error.error.error || 'Request failed';
          this.successMsg = '';
        }
      });
  }
}
