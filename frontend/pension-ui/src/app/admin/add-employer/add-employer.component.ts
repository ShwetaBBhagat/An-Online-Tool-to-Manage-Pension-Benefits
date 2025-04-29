import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';  // Import if you are using [routerLink]

@Component({
  selector: 'app-add-employer',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule, RouterModule],
  templateUrl: './add-employer.component.html',
  styleUrls: ['./add-employer.component.css']
})
export class AddEmployerComponent {
  employer = {
    name: '',
    email: '',
    contact_number: '',
    address: ''
  };

  successMsg: string = '';
  errorMsg: string = '';
  loading: boolean = false;

  constructor(private http: HttpClient) {}

  submitForm() {
    const token = localStorage.getItem('adminToken');

    if (!token) {
      this.errorMsg = "Unauthorized. Please login again.";
      return;
    }

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });

    this.loading = true; // Start loading

    this.http.post<any>('http://127.0.0.1:5000/api/admin/add-employers', this.employer, { headers }).subscribe({
      next: (res) => {
        this.successMsg = res.message;
        this.errorMsg = '';
        this.employer = { name: '', email: '', contact_number: '', address: '' }; // Clear form
        this.loading = false;
      },
      error: (err) => {
        console.error('Error adding employer:', err);
        this.successMsg = '';
        this.errorMsg = err.error?.error || 'Something went wrong. Please try again.';
        this.loading = false;
      }
    });
  }
}
