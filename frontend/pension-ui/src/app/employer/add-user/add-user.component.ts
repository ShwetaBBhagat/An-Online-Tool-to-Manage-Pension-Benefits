import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-add-user',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule, RouterModule],
  templateUrl: './add-user.component.html',
  styleUrls: ['./add-user.component.css']
})
export class AddUserComponent {
  name = '';
  email = '';
  salary = '';
  dateOfBirth = '';
  investmentType = 'Medium';

  successMsg = '';
  errorMsg = '';

  constructor(private http: HttpClient) {}

  addUser() {
    const token = localStorage.getItem('employerToken');
    const headers = { Authorization: `Bearer ${token}` };

    this.http.post<any>('http://127.0.0.1:5000/api/employer/add-user', {
      name: this.name,
      email: this.email,
      salary: this.salary,
      date_of_birth: this.dateOfBirth,
      investment_type: this.investmentType
    }, { headers }).subscribe({
      next: (res) => {
        this.successMsg = res.message + ` (Auto Enrolled: ${res.auto_enrolled ? 'Yes' : 'No'})`;
        this.errorMsg = '';
        this.resetForm();
      },
      error: (err) => {
        this.errorMsg = err.error?.error || 'Failed to add user.';
        this.successMsg = '';
      }
    });
  }

  resetForm() {
    this.name = '';
    this.email = '';
    this.salary = '';
    this.dateOfBirth = '';
    this.investmentType = 'Medium';
  }
}
