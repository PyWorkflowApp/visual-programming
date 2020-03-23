import * as React from 'react';


export class CustomLinkWidget extends React.Component<{ model: CustomLinkModel; path: string }> {

  path: SVGPathElement;
	circle: SVGCircleElement;
	callback: () => any;
	percent: number;
	handle: any;
	mounted: boolean;
  radius: number;

	constructor(props) {
		super(props);
		this.percent = 0;
    this.radius = 5;
	}

	componentDidMount() {
		this.mounted = true;
		this.callback = () => {
			if (!this.circle || !this.path) {
				return;
			}

			this.percent += 2;
			if (this.percent > 100) {
				this.percent = 0;
			}

			let point = this.path.getPointAtLength(this.path.getTotalLength() * (this.percent / 100.0));

			this.circle.setAttribute('cx', '' + point.x);
			this.circle.setAttribute('cy', '' + point.y);

			if (this.mounted) {
				requestAnimationFrame(this.callback);
			}
		};
		requestAnimationFrame(this.callback);
	}

	componentWillUnmount() {
		this.mounted = false;
	}

	render() {
		return (
			<>
				<path
					fill="none"
					ref={ref => {
						this.path = ref;
					}}
					strokeWidth={this.props.model.getOptions().width}
					stroke="rgba(255,0,0,0.5)"
					d={this.props.path}
				/>
			</>
		);
	}

  isPointDefault(point: Point) {
    return point.x === 0 && point.y === 0;
  }

}
