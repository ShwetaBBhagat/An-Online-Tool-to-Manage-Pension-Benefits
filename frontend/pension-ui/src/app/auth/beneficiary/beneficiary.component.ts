import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms'; 
import { CommonModule } from '@angular/common';
import { ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-beneficiary',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './beneficiary.component.html',
  styleUrls: ['./beneficiary.component.css']
})

export class BeneficiaryComponent {
  @ViewChild('beneficiaryForm') beneficiaryFormRef!: NgForm;

  beneficiary = {
    full_name: '',
    relationship: '',
    percentage: 100
  };

  successMsg = '';
  errorMsg = '';


  constructor(private http: HttpClient) {
    this.loadBeneficiary();
  }

  loadBeneficiary() {
    const token = localStorage.getItem('userToken');
    this.http.get<any>('http://127.0.0.1:5000/api/auth/user/beneficiary', {
      headers: { Authorization: `Bearer ${token}` }
    }).subscribe({
      next: res => {
        this.beneficiary = res; // pre-fill form
      },
      error: err => {
        if (err.status !== 404) {
          this.errorMsg = 'Failed to load beneficiary info.';
        }
      }
    });
  }

  saveBeneficiary() {
    const token = localStorage.getItem('userToken');
    this.http.post('http://127.0.0.1:5000/api/auth/user/beneficiary', this.beneficiary, {
      headers: { Authorization: `Bearer ${token}` }
    }).subscribe({
      next: (res: any) => {
        this.successMsg = res.message;
        this.errorMsg = '';

        // Reset the form data and UI
        this.beneficiary = {
          full_name: '',
          relationship: '',
          percentage: 100
        };
        this.beneficiaryFormRef.resetForm(this.beneficiary);

      },
      error: err => {
        this.errorMsg = err.error?.error || 'Failed to save beneficiary.';
        this.successMsg = '';
      }
    });
  }
}
