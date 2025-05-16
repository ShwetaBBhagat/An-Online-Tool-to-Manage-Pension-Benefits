import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmployerResetPasswordComponent } from './reset-password.component';

describe('EmployerResetPasswordComponent', () => {
  let component: EmployerResetPasswordComponent;
  let fixture: ComponentFixture<EmployerResetPasswordComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EmployerResetPasswordComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EmployerResetPasswordComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
