import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewEmployersComponent } from './view-employers.component';

describe('ViewEmployersComponent', () => {
  let component: ViewEmployersComponent;
  let fixture: ComponentFixture<ViewEmployersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewEmployersComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewEmployersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
