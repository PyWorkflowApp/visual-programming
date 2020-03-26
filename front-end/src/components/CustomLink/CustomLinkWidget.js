import * as React from 'react';

export class CustomLinkWidget extends React.Component<{ model: CustomLinkModel; path: string }> {

  path: SVGPathElement;
	callback: () => any;
	percent: number;
	handle: any;
	mounted: boolean;

	constructor(props) {
		super(props);
		this.percent = 0;
	}

	componentDidMount() {
		this.mounted = true;
		this.callback = () => {
			if (!this.path) {
				return;
			}

			this.percent += 2;
			if (this.percent > 100) {
				this.percent = 0;
			}

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

}
