difference() {
	cube(size = [25, 25, 75]);
	union() {
		union() {
			translate(v = [0, -1.0, 25]) {
				cube(size = [25, 2, 2]);
			}
			translate(v = [0, 24.0, 25]) {
				cube(size = [25, 2, 2]);
			}
			translate(v = [-1.0, 0, 25]) {
				cube(size = [2, 25, 2]);
			}
			translate(v = [24.0, 0, 25]) {
				cube(size = [2, 25, 2]);
			}
		}
		union() {
			translate(v = [0, -1.0, 50]) {
				cube(size = [25, 2, 2]);
			}
			translate(v = [0, 24.0, 50]) {
				cube(size = [25, 2, 2]);
			}
			translate(v = [-1.0, 0, 50]) {
				cube(size = [2, 25, 2]);
			}
			translate(v = [24.0, 0, 50]) {
				cube(size = [2, 25, 2]);
			}
		}
	}
}
