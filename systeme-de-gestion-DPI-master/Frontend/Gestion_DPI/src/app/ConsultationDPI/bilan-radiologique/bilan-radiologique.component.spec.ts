import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BilanRadiologiqueComponent } from './bilan-radiologique.component';

describe('BilanRadiologiqueComponent', () => {
  let component: BilanRadiologiqueComponent;
  let fixture: ComponentFixture<BilanRadiologiqueComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BilanRadiologiqueComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BilanRadiologiqueComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
