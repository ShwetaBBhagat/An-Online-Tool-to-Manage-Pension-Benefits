import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-add-employer',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
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

  successMsg = '';
  errorMsg = '';

  constructor(private http: HttpClient) {}

  submitForm() {
    const token = localStorage.getItem('adminToken');
    const headers = { Authorization: `Bearer ${token}` };

    this.http.post<any>('http://127.0.0.1:5000/api/admin/add-employers', this.employer, { headers }).subscribe({
      next: (res) => {
        this.successMsg = res.message;
        this.errorMsg = '';
        this.employer = { name: '', email: '', contact_number: '', address: '' };
      },
      error: (err) => {
        this.successMsg = '';
        this.errorMsg = err.error?.error || 'Something went wrong';
      }
    });
  }
}
