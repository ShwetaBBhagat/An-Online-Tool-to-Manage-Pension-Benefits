import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-upload-document',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './upload-document.component.html',
  styleUrls: ['./upload-document.component.css']
})
export class UploadDocumentComponent {
  selectedFile: File | null = null;
  successMsg = '';
  errorMsg = '';

  constructor(private http: HttpClient) {}

  onFileSelected(event: any) {
    const file = event.target.files[0];

    if (file) {
      const allowedTypes = ['application/pdf', 'image/png', 'image/jpeg'];
      if (!allowedTypes.includes(file.type)) {
        this.errorMsg = 'Only PDF, PNG, JPG, JPEG files are allowed.';
        this.selectedFile = null;
      } else {
        this.selectedFile = file;
        this.errorMsg = '';
      }
    }
  }

  uploadDocument() {
    if (!this.selectedFile) {
      this.errorMsg = 'Please select a valid file.';
      return;
    }

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    const token = localStorage.getItem('userToken');

    this.http.post<any>('http://127.0.0.1:5000/api/auth/user/upload-document', formData, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }).subscribe({
      next: (res) => {
        this.successMsg = res.message;
        this.errorMsg = '';
        this.selectedFile = null;
      },
      error: (err) => {
        this.errorMsg = err.error?.error || 'Upload failed';
        this.successMsg = '';
      }
    });
  }
}
